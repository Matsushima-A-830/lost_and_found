import * as React from "react";
import { cn } from "../lib/utils";

// shadcn/ui Button
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => (
    <button
      className={cn(
        "px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 transition",
        className
      )}
      ref={ref}
      {...props}
    />
  )
);
Button.displayName = "Button";
export { Button };
