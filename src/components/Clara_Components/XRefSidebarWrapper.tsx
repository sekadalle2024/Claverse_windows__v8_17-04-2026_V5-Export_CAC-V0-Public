/**
 * XRefSidebarWrapper Component
 * 
 * Wrapper qui écoute les événements du menu.js et affiche le XRefSidebar
 * Gère la communication entre le menu contextuel JavaScript et le composant React
 */

import React, { useState, useEffect } from 'react';
import XRefSidebar from './XRefSidebar';

interface XRefDocument {
  crossRef: string;
  document: string;
  client?: string;
  exercice?: string;
  cycle?: string;
  dateUpload?: string;
  fileId?: string;
  fileUrl?: string;
}

interface XRefOpenEvent {
  documents: XRefDocument[];
  searchTerm?: string;
  title?: string;
}

const XRefSidebarWrapper: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [documents, setDocuments] = useState<XRefDocument[]>([]);
  const [title, setTitle] = useState<string>('Cross-Références Documentaires');

  useEffect(() => {
    // Écouter l'événement d'ouverture depuis menu.js
    const handleOpen = (event: Event) => {
      const customEvent = event as CustomEvent<XRefOpenEvent>;
      const { documents: docs, searchTerm, title: eventTitle } = customEvent.detail;
      
      console.log('📋 [XRefWrapper] Événement reçu:', customEvent.detail);
      
      setDocuments(docs || []);
      setTitle(eventTitle || (searchTerm ? `Résultats pour "${searchTerm}"` : 'Cross-Références Documentaires'));
      setIsOpen(true);
    };

    // Écouter l'événement de fermeture
    const handleClose = () => {
      console.log('📋 [XRefWrapper] Fermeture demandée');
      setIsOpen(false);
    };

    document.addEventListener('xref:open', handleOpen);
    document.addEventListener('xref:close', handleClose);

    return () => {
      document.removeEventListener('xref:open', handleOpen);
      document.removeEventListener('xref:close', handleClose);
    };
  }, []);

  /**
   * Gérer le clic sur un document
   * Appelle le workflow n8n pour récupérer l'URL si nécessaire
   */
  const handleDocumentClick = async (doc: XRefDocument) => {
    console.log('📄 [XRefWrapper] Document sélectionné:', doc);
    
    // Si on a déjà une URL, l'ouvrir directement
    if (doc.fileUrl) {
      window.open(doc.fileUrl, '_blank');
      return;
    }

    // Si on a un fileId, ouvrir dans Google Drive
    if (doc.fileId) {
      window.open(`https://drive.google.com/file/d/${doc.fileId}/view`, '_blank');
      return;
    }

    // Sinon, appeler le workflow n8n pour rechercher le document
    try {
      console.log('🔍 [XRefWrapper] Recherche du document dans Google Drive...');
      
      const response = await fetch('https://hkj0631c.rpcl.app/webhook/cross_reference', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          index: doc.crossRef,
          document: doc.document,
          client: doc.client,
          exercice: doc.exercice,
          cycle: doc.cycle
        })
      });
      
      if (!response.ok) {
        throw new Error(`Erreur HTTP ${response.status}`);
      }
      
      const result = await response.json();
      console.log('✅ [XRefWrapper] Résultat de la recherche:', result);
      
      if (result.success && result.fileUrl) {
        window.open(result.fileUrl, '_blank');
        
        // Notifier le succès
        document.dispatchEvent(new CustomEvent('xref:document:opened', {
          detail: { document: doc, fileUrl: result.fileUrl }
        }));
      } else {
        console.warn('⚠️ [XRefWrapper] Document non trouvé dans Google Drive');
        alert(`⚠️ Document "${doc.document}" non trouvé dans Google Drive.\n\nVérifiez que le document a bien été uploadé via le formulaire n8n.`);
      }
    } catch (error) {
      console.error('❌ [XRefWrapper] Erreur recherche document:', error);
      alert(`❌ Erreur lors de la recherche du document:\n${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    }
  };

  /**
   * Gérer la prévisualisation d'un document
   */
  const handleDocumentPreview = async (doc: XRefDocument) => {
    console.log('👁️ [XRefWrapper] Prévisualisation demandée:', doc);
    
    // Si on a une URL, l'ouvrir dans un nouvel onglet
    if (doc.fileUrl) {
      window.open(doc.fileUrl, '_blank');
      return;
    }

    // Si on a un fileId, ouvrir la prévisualisation Google Drive
    if (doc.fileId) {
      window.open(`https://drive.google.com/file/d/${doc.fileId}/preview`, '_blank');
      return;
    }

    // Sinon, même logique que handleDocumentClick
    await handleDocumentClick(doc);
  };

  /**
   * Gérer la fermeture de la sidebar
   */
  const handleClose = () => {
    console.log('📋 [XRefWrapper] Fermeture de la sidebar');
    setIsOpen(false);
    
    // Notifier la fermeture
    document.dispatchEvent(new CustomEvent('xref:closed'));
  };

  return (
    <XRefSidebar
      isOpen={isOpen}
      onClose={handleClose}
      documents={documents}
      title={title}
      onDocumentClick={handleDocumentClick}
      onDocumentPreview={handleDocumentPreview}
    />
  );
};

export default XRefSidebarWrapper;
