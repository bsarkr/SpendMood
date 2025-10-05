import { format } from 'date-fns';
import { useEffect, useState } from 'react';

function PurchaseDetailModal({ entry, onClose, position }) {
    const [modalStyle, setModalStyle] = useState({});

    useEffect(() => {
        if (!entry) return;

        const modalWidth = 400;
        const modalMaxHeight = 500;
        const padding = 20;
        const bottomPadding = 60; // Extra padding from bottom

        const openLeft = position.x > window.innerWidth / 2;

        let top = position.y;

        // If modal would go below viewport, move it up with extra bottom padding
        if (top + modalMaxHeight > window.innerHeight - bottomPadding) {
            top = window.innerHeight - modalMaxHeight - bottomPadding;
        }

        if (top < padding) {
            top = padding;
        }

        let horizontalPos;
        if (openLeft) {
            horizontalPos = {
                right: (window.innerWidth - position.x + padding) + 'px'
            };
            if (window.innerWidth - position.x + padding + modalWidth > window.innerWidth) {
                horizontalPos = { left: padding + 'px' };
            }
        } else {
            horizontalPos = {
                left: (position.x + padding) + 'px'
            };
            if (position.x + padding + modalWidth > window.innerWidth) {
                horizontalPos = { right: padding + 'px' };
            }
        }

        setModalStyle({
            top: top + 'px',
            ...horizontalPos
        });
    }, [entry, position]);

    if (!entry) return null;

    return (
        <>
            <div className="modal-backdrop" onClick={onClose} />
            <div
                className="purchase-modal"
                style={modalStyle}
            >
                <button className="modal-close" onClick={onClose}>×</button>

                <div className={`mood-badge mood-${entry.mood.toLowerCase()}`}>
                    {entry.mood}
                </div>

                <div className="modal-section">
                    <div className="modal-label">TIME</div>
                    <div className="modal-value">{format(new Date(entry.timestamp), 'EEEE, MMMM d, yyyy · h:mm a')}</div>
                </div>

                <div className="modal-section">
                    <div className="modal-label">PURCHASE</div>
                    <div className="modal-value">{entry.item}</div>
                </div>

                <div className="modal-section">
                    <div className="modal-label">AMOUNT</div>
                    <div className="modal-value modal-amount">${entry.amount.toFixed(2)}</div>
                </div>

                <div className="modal-section">
                    <div className="modal-label">CATEGORY</div>
                    <div className="modal-value">{entry.category}</div>
                </div>

                <div className="modal-section">
                    <div className="modal-label">WHAT YOU SAID</div>
                    <div className="modal-original-text">{entry.reason}</div>
                </div>
            </div>
        </>
    );
}

export default PurchaseDetailModal;