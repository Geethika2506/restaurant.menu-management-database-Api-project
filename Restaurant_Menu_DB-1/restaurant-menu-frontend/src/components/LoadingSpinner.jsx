import React from "react";

const LoadingSpinner = ({ size = "medium", color = "blue" }) => {
  const sizes = {
    small: "h-6 w-6",
    medium: "h-10 w-10",
    large: "h-16 w-16",
  };

  const colors = {
    blue: "border-blue-600",
    gray: "border-gray-600",
    red: "border-red-600",
  };

  return (
    <div className="flex justify-center items-center">
      <div
        className={`animate-spin ${sizes[size]} border-4 border-t-transparent rounded-full ${colors[color]}`}
      ></div>
    </div>
  );
};

export default LoadingSpinner;
