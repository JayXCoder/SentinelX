import { AnnouncementBar } from '@/components/marketing/announcement-bar';
import { BenefitsSection } from '@/components/marketing/benefits-section';
import { CtaSection } from '@/components/marketing/cta-section';
import { FaqSection } from '@/components/marketing/faq-section';
import { HeroSection } from '@/components/marketing/hero-section';
import { PlatformSection } from '@/components/marketing/platform-section';
import { SiteFooter } from '@/components/marketing/site-footer';
import { SiteHeader } from '@/components/marketing/site-header';
import { StepsSection } from '@/components/marketing/steps-section';
import { UseCaseSection } from '@/components/marketing/use-case-section';

export default function HomePage() {
  return (
    <div className="min-h-dvh bg-background text-foreground">
      <AnnouncementBar />
      <SiteHeader />
      <main>
        <HeroSection />
        <UseCaseSection />
        <StepsSection />
        <BenefitsSection />
        <PlatformSection />
        <FaqSection />
        <CtaSection />
      </main>
      <SiteFooter />
    </div>
  );
}
