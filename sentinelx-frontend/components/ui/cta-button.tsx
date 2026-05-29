import Link from 'next/link';
import { cn } from '@/lib/utils';

type CtaVariant = 'solid' | 'warm' | 'secondary' | 'ghost';
type CtaSize = 'sm' | 'md' | 'lg';

const sizeClass: Record<CtaSize, string> = {
  sm: 'btn-cta--sm',
  md: 'btn-cta--md',
  lg: 'btn-cta--lg',
};

type CtaButtonProps = {
  href: string;
  children: React.ReactNode;
  variant?: CtaVariant;
  size?: CtaSize;
  className?: string;
};

export function CtaButton({
  href,
  children,
  variant = 'solid',
  size = 'md',
  className,
}: CtaButtonProps) {
  return (
    <Link
      href={href}
      className={cn(
        variant === 'secondary' && 'btn-cta-secondary',
        variant === 'ghost' && 'btn-cta-ghost',
        (variant === 'solid' || variant === 'warm') && 'btn-cta',
        (variant === 'solid' || variant === 'warm') && sizeClass[size],
        variant === 'warm' && 'btn-cta--warm',
        className,
      )}
    >
      {children}
    </Link>
  );
}
