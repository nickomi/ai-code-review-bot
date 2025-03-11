import { useState, useEffect } from "react";

export default function ReviewDashboard() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch("http://your-api-endpoint/reviews")
      .then((response) => response.json())
      .then((data) => setReviews(data))
      .catch((error) => console.error("Error fetching reviews:", error));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">AI Code Review Dashboard</h1>
      <ul>
        {reviews.map((review, index) => (
          <li key={index} className="border p-2 my-2 rounded">
            <p><strong>PR:</strong> <a href={review.pr_url} target="_blank" rel="noopener noreferrer">{review.pr_url}</a></p>
            <p><strong>Review:</strong> {review.review}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
