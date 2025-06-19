import * as React from "react";
import { cn } from "../lib/utils";

// shadcn/ui Input
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => (
    <input
      className={cn(
        "border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400",
        className
      )}
      ref={ref}
      {...props}
    />
  )
);
Input.displayName = "Input";
export { Input };
