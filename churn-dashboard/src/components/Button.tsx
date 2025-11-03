import React from 'react';

interface ButtonProps {
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
  fullWidth?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  onClick,
  disabled = false,
  variant = 'primary',
  fullWidth = false,
  children
}) => {
  const baseStyle = "px-4 py-2 rounded font-medium transition";
  const variantStyle = variant === 'primary' 
    ? "bg-blue-600 hover:bg-blue-700 text-white" 
    : "bg-gray-700 hover:bg-gray-600 text-white";
  const fullWidthStyle = fullWidth ? "w-full" : "";
  const disabledStyle = disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer";

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variantStyle} ${fullWidthStyle} ${disabledStyle}`}
    >
      {children}
    </button>
  );
};
