// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'PHYSICAL AI & HUMANOID ROBOTICS',
  tagline: 'A Hands-On Guide to Humanoid Robotics, ROS 2, Simulation, and AI Integration',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-docusaurus-site.example.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages deployment, it is often '/<org-name>/<repo-name>/'
  baseUrl: '/physical-ai-humanoid-robotics/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-username', // Usually your GitHub org/user name.
  projectName: 'physical-ai-humanoid-robotics', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'PHYSICAL AI & HUMANOID ROBOTICS',
        logo: {
          alt: 'Physical AI & Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'module_0_overview',
            position: 'left',
            label: 'Home / Overview',
          },
          {
            type: 'doc',
            docId: 'module_1/module_1_0',
            position: 'left',
            label: 'Module 1 – The Robotic Nervous System',
          },
          {
            type: 'doc',
            docId: 'module_2/module_2_0',
            position: 'left',
            label: 'Module 2 – The Digital Twin',
          },
          {
            type: 'doc',
            docId: 'module_3/module_3_0',
            position: 'left',
            label: 'Module 3 – The AI-Robot Brain',
          },
          {
            type: 'doc',
            docId: 'module_4/module_4_0',
            position: 'left',
            label: 'Module 4 – Vision-Language-Action',
          },
          {
            type: 'doc',
            docId: 'module_1/module_1_lab',
            position: 'left',
            label: 'Labs',
          },
          {
            type: 'doc',
            docId: 'module_2/module_2_lab',
            position: 'left',
            label: 'Exercises',
          },
          {
            type: 'doc',
            docId: 'module_4/module_4_4',
            position: 'left',
            label: 'References',
          },
          {
            type: 'doc',
            docId: 'module_4/module_4_lab',
            position: 'left',
            label: 'About / Authors',
          },
          {
            href: 'https://github.com/facebook/docusaurus',
            label: 'GitHub',
            position: 'right',
          },
          {
            type: 'search',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Textbook',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;