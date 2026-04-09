export const seoKeywords = [
  'Grove',
  'semantic git helper',
  'conventional commits',
  'conventional branches',
  'git commit helper',
  'git branch helper',
  'python CLI',
  'developer tool',
  'Git workflow documentation',
  'semantic commits',
] as const;

export const buildStructuredData = ({
  pageTitle,
  pageDescription,
  canonicalUrl,
  docsUrl,
  ogImageUrl,
  githubUrl,
  version,
}: {
  pageTitle: string;
  pageDescription: string;
  canonicalUrl: string;
  docsUrl: string;
  ogImageUrl: string;
  githubUrl: string;
  version: string;
}) => [
  {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Grove Documentation',
    url: docsUrl,
    description: pageDescription,
    inLanguage: 'en',
    image: ogImageUrl,
  },
  {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Grove',
    applicationCategory: 'DeveloperApplication',
    operatingSystem: 'Windows, macOS, Linux',
    softwareVersion: version,
    description: pageDescription,
    url: canonicalUrl,
    downloadUrl: githubUrl,
    screenshot: ogImageUrl,
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    author: {
      '@type': 'Person',
      name: 'Vinícius Costa',
      url: 'https://viniciusnevescosta.com',
    },
  },
  {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: pageTitle,
    description: pageDescription,
    mainEntityOfPage: canonicalUrl,
    author: {
      '@type': 'Person',
      name: 'Vinícius Costa',
      url: 'https://viniciusnevescosta.com',
    },
    about: {
      '@type': 'SoftwareSourceCode',
      name: 'Grove',
      codeRepository: githubUrl,
      programmingLanguage: 'Python',
      runtimePlatform: 'Python 3',
    },
    image: ogImageUrl,
    inLanguage: 'en',
  },
];
