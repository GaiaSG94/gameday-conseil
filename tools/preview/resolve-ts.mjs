/* Node resolver hook for the local preview bench: lets the app's own modules
   (written for the bundler, without file extensions) load under
   `node --experimental-strip-types`. Dev tooling only, never shipped. */
import { existsSync } from 'node:fs';
import { registerHooks } from 'node:module';
import { fileURLToPath } from 'node:url';

registerHooks({
  resolve(specifier, context, nextResolve) {
    try {
      return nextResolve(specifier, context);
    } catch (err) {
      if (specifier.startsWith('.') && !/\.[cm]?[jt]sx?$/.test(specifier)) {
        const parent = context.parentURL ?? 'file:///';
        for (const ext of ['.ts', '.tsx']) {
          const url = new URL(specifier + ext, parent);
          if (existsSync(fileURLToPath(url))) {
            return nextResolve(specifier + ext, context);
          }
        }
      }
      throw err;
    }
  },
});
