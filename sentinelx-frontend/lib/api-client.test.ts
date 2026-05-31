import { describe, expect, it } from 'vitest';

import { getApiErrorMessage } from './api-client';

describe('getApiErrorMessage', () => {
  it('returns message from ApiError shape', () => {
    expect(getApiErrorMessage({ message: 'Request failed: 503', status: 503 })).toBe(
      'Request failed: 503',
    );
  });

  it('returns Error message', () => {
    expect(getApiErrorMessage(new Error('network down'))).toBe('network down');
  });

  it('returns fallback for unknown values', () => {
    expect(getApiErrorMessage(null)).toBe('Request failed');
  });
});
