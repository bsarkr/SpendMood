import { useState } from 'react';

const API_BASE = 'http://localhost:8000/api';

function NessieSync({ onSyncComplete }) {
    const [isImporting, setIsImporting] = useState(false);
    const [importResult, setImportResult] = useState(null);

    const handleImport = async () => {
        setIsImporting(true);
        setImportResult(null);

        try {
            const response = await fetch(`${API_BASE}/nessie/import/68e1f0fa9683f20dd519a6af`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Import failed');
            }

            const data = await response.json();
            setImportResult(data);

            if (onSyncComplete) {
                onSyncComplete(data);
            }

            setTimeout(() => window.location.reload(), 2000);
        } catch (error) {
            console.error('Nessie import error:', error);
            setImportResult({ error: 'Failed to import transactions' });
        } finally {
            setIsImporting(false);
        }
    };

    return (
        <div className="nessie-sync">
            <button
                className="sync-btn"
                onClick={handleImport}
                disabled={isImporting}
            >
                {isImporting ? 'Importing...' : 'Import Capital One Demo Data'}
            </button>

            {importResult && (
                <div className={`sync-result ${importResult.error ? 'error' : 'success'}`}>
                    {importResult.error
                        ? importResult.error
                        : `Imported ${importResult.imported} purchases. ${importResult.analyzed} flagged for review.`}
                </div>
            )}
        </div>
    );
}

export default NessieSync;