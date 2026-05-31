'use client';

import { useRouter } from 'next/navigation';
import { Modal } from '@/components/ui/modal';
import { Input } from '@/components/ui/input';
import { useDashboardStore } from '@/stores/dashboard-store';

type SearchDialogProps = {
  open: boolean;
  onClose: () => void;
};

export function SearchDialog({ open, onClose }: SearchDialogProps) {
  const router = useRouter();
  const searchQuery = useDashboardStore((state) => state.searchQuery);
  const setSearchQuery = useDashboardStore((state) => state.setSearchQuery);

  const submit = () => {
    const query = searchQuery.trim();
    if (!query) {
      onClose();
      return;
    }
    setSearchQuery(query);
    router.push(`/dashboard/threat-feed?q=${encodeURIComponent(query)}`);
    onClose();
  };

  return (
    <Modal open={open} title="Search intelligence" description="Search titles, summaries, entities, and evidence." onClose={onClose}>
      <form
        className="space-y-4"
        onSubmit={(event) => {
          event.preventDefault();
          submit();
        }}
      >
        <Input
          label="Query"
          value={searchQuery}
          onChange={(event) => setSearchQuery(event.target.value)}
          placeholder="e.g. CVE, vendor outage, competitor pricing"
          autoFocus
        />
        <div className="flex justify-end gap-2">
          <button type="button" onClick={onClose} className="btn-cta-secondary">
            Cancel
          </button>
          <button type="submit" className="btn-cta btn-cta--warm">
            Search threat feed
          </button>
        </div>
      </form>
    </Modal>
  );
}
