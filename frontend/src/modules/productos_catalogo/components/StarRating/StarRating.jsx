import React, { useState } from 'react';
import './StarRating.css';

const StarRating = ({ rating = 0, onRatingChange, readOnly = false }) => {
    const [hover, setHover] = useState(0);

    return (
        <div className={`star-rating ${readOnly ? 'readonly' : 'interactive'}`}>
            {[1, 2, 3, 4, 5].map((star) => {
                const isActive = star <= (hover || rating);
                return (
                    <button
                        type="button"
                        key={star}
                        className={`star-button ${isActive ? 'active' : ''}`}
                        onClick={() => !readOnly && onRatingChange && onRatingChange(star)}
                        onMouseEnter={() => !readOnly && setHover(star)}
                        onMouseLeave={() => !readOnly && setHover(0)}
                        disabled={readOnly}
                        aria-label={`${star} estrella${star !== 1 ? 's' : ''}`}
                    >
                        <span className="star-icon">★</span>
                    </button>
                );
            })}
        </div>
    );
};

export default StarRating;
