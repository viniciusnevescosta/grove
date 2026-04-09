const storageKey = 'grove-theme';
const mistThemeColor = 'oklch(95.1% 0.009 78.3)';
const nightThemeColor = 'oklch(28.1% 0.016 248.4)';

const toggle = document.querySelector<HTMLButtonElement>('#theme-toggle');
const themeColor = document.querySelector<HTMLMetaElement>('meta[name="theme-color"]');
const root = document.documentElement;
const siteHeader = document.querySelector<HTMLElement>('.site-header');

const getMode = () => {
  const saved = window.localStorage.getItem(storageKey);
  if (saved === 'night' || saved === 'mist') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'night' : 'mist';
};

const renderTheme = (mode: 'mist' | 'night') => {
  const isNight = mode === 'night';
  root.dataset.theme = isNight ? 'still-orbit-night' : 'still-orbit-mist';
  root.classList.toggle('dark', isNight);
  window.localStorage.setItem(storageKey, mode);

  if (toggle) {
    const nextLabel = isNight ? 'light mode' : 'dark mode';
    toggle.setAttribute('aria-label', `Switch to ${nextLabel}`);
    toggle.setAttribute('title', `Switch to ${nextLabel}`);
  }

  if (themeColor) {
    themeColor.setAttribute('content', isNight ? nightThemeColor : mistThemeColor);
  }
};

toggle?.addEventListener('click', () => {
  renderTheme(getMode() === 'night' ? 'mist' : 'night');
});

document.addEventListener('keydown', (event) => {
  if (
    event.key.toLowerCase() === 'd' &&
    !event.metaKey &&
    !event.ctrlKey &&
    !event.altKey &&
    !(event.target instanceof HTMLInputElement) &&
    !(event.target instanceof HTMLTextAreaElement)
  ) {
    renderTheme(getMode() === 'night' ? 'mist' : 'night');
  }
});

const copyableBlocks = Array.from(document.querySelectorAll<HTMLElement>('.code-block, [data-copyable]'));

const copyText = async (text: string) => {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', 'true');
  textarea.style.position = 'absolute';
  textarea.style.left = '-9999px';
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand('copy');
  textarea.remove();
};

copyableBlocks.forEach((block) => {
  const code = block.querySelector('code');
  if (!code || block.querySelector('.code-copy')) return;

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'code-copy';
  button.textContent = block.dataset.copyLabel ?? 'Copy';
  button.setAttribute('aria-label', block.dataset.copyLabel ?? 'Copy code');

  button.addEventListener('click', async () => {
    const originalLabel = block.dataset.copyLabel ?? 'Copy';

    try {
      await copyText(code.textContent ?? '');
      button.textContent = 'Copied';
      button.classList.add('is-copied');
    } catch {
      button.textContent = 'Failed';
    }

    window.setTimeout(() => {
      button.textContent = originalLabel;
      button.classList.remove('is-copied');
    }, 1600);
  });

  block.append(button);
});

const tocLinks = Array.from(document.querySelectorAll<HTMLAnchorElement>('[data-toc-link]'));
const observedTargets = tocLinks
  .map((link) => {
    const id = link.getAttribute('href')?.replace('#', '');
    return id ? document.getElementById(id) : null;
  })
  .filter((element): element is HTMLElement => element instanceof HTMLElement);

if (tocLinks.length && observedTargets.length) {
  const setActiveLink = (id: string) => {
    tocLinks.forEach((link) => {
      const isActive = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('is-active', isActive);
      if (isActive) {
        link.setAttribute('aria-current', 'true');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  };

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => {
          if (a.boundingClientRect.top === b.boundingClientRect.top) {
            return b.intersectionRatio - a.intersectionRatio;
          }
          return a.boundingClientRect.top - b.boundingClientRect.top;
        })[0];

      if (visible?.target instanceof HTMLElement && visible.target.id) {
        setActiveLink(visible.target.id);
      }
    },
    {
      rootMargin: '-12% 0px -74% 0px',
      threshold: [0.1, 0.25, 0.45, 0.7],
    },
  );

  observedTargets.forEach((section) => observer.observe(section));

  tocLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
      const id = link.getAttribute('href')?.replace('#', '');
      if (!id) return;

      const target = document.getElementById(id);
      if (!target) return;

      event.preventDefault();

      const headerOffset = siteHeader?.getBoundingClientRect().height ?? 0;
      const top = target.getBoundingClientRect().top + window.scrollY - headerOffset - 6;

      window.scrollTo({
        top,
        behavior: 'smooth',
      });

      history.replaceState(null, '', `#${id}`);
      setActiveLink(id);
    });
  });

  const currentHash = window.location.hash.replace('#', '');
  if (currentHash) {
    setActiveLink(currentHash);
  } else if (observedTargets[0]?.id) {
    setActiveLink(observedTargets[0].id);
  }
}

renderTheme(getMode() as 'mist' | 'night');
