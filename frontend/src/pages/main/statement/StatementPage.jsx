import { useEffect } from 'react';
import DocViewer, { PDFRenderer } from '@cyntler/react-doc-viewer';
import styles from './StatementPage.module.scss';

const StatementPage = () => {
  const docs = [{ uri: '/documents/privacy_policy.pdf' }];

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className={styles.container}>
      <DocViewer
        documents={docs}
        pluginRenderers={[PDFRenderer]}
        initialActiveDocument={docs[0]}
        style={{ width: 1000, height: 1000 }}
        config={{
          header: {
            disableHeader: false,
            disableFileName: true,
            retainURLParams: false,
          },

          pdfZoom: {
            defaultZoom: 1.1,
            zoomJump: 0.2,
          },
          pdfVerticalScrollByDefault: true,
        }}
      />
    </div>
  );
};

export default StatementPage;
