import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'PHYSICAL AI & HUMANOID ROBOTICS',
  tagline: 'A Hands-On Guide to Humanoid Robotics, ROS 2, Simulation, and AI Integration',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://physical-ai-humanoid-robotics-book.com',
  baseUrl: '/',

  organizationName: 'physical-ai-humanoid-robotics',
  projectName: 'physical-ai-humanoid-robotics',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        docsRouteBasePath: '/',
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/physical-ai-humanoid-robotics/physical-ai-humanoid-robotics/edit/main/',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [],

  themeConfig: {
    image: 'img/physical-ai-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
  title: 'PHYSICAL AI & HUMANOID ROBOTICS',
  items: [
    { type: 'doc', docId: 'module_0_overview', label: 'Modules / Overview', position: 'left' },
    { href: 'https://github.com/physical-ai-humanoid-robotics/physical-ai-humanoid-robotics', label: 'GitHub', position: 'right' },
    { type: 'search', position: 'right' },
  ],
},

  footer: {
  style: 'dark',
  links: [
    {
      title: 'Resources',
      items: [
        {
          label: 'Modules Overview',
          to: '/docs/module_0_overview'
        },
        {
          label: 'GitHub Repository',
          href: 'https://github.com/physical-ai-humanoid-robotics/physical-ai-humanoid-robotics'
        },
        {
          label: 'ROS Documentation',
          href: 'https://docs.ros.org/'
        }
      ]
    }
  ],
  copyright:
    '© 2025 PHYSICAL AI & HUMANOID ROBOTICS — Authored by Areeba Hammad 💗'
},


    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml', 'docker', 'cpp', 'csharp', 'typescript'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;