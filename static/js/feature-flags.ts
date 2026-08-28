export type FrontendEnvironment = 'production' | 'local' | 'alpha';

export type FeatureFlags = Record<string, Partial<Record<FrontendEnvironment, boolean>>>;

let currentEnvironment: FrontendEnvironment = 'production';
let featureFlags: FeatureFlags = {};

export function initializeFeatureFlags(flags: FeatureFlags | undefined, environment: string | undefined) {
  featureFlags = flags ?? {};

  if (environment === 'production' || environment === 'local' || environment === 'alpha') {
    currentEnvironment = environment;
  }
}

export function isFeatureEnabled(flagName: string): boolean {
  const flagConfig = featureFlags[flagName];
  if (!flagConfig) {
    return false;
  }

  return !!flagConfig[currentEnvironment];
}
