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
  markdown: {
    mermaid: true,
    parseFrontMatter: undefined,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

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
    // Custom webpack configuration plugin
    function customWebpackPlugin() {
      return {
        name: 'custom-webpack-config',
        configureWebpack(config, isServer) {
          const webpack = require('webpack');

          return {
            resolve: {
              fallback: {
                fs: false,
                path: require.resolve('path-browserify'),
                os: require.resolve('os-browserify/browser'),
                crypto: require.resolve('crypto-browserify'),
                stream: require.resolve('stream-browserify'),
                assert: require.resolve('assert/'),
                util: require.resolve('util/'),
                buffer: require.resolve('buffer/'),
                constants: require.resolve('constants-browserify'),
                process: require.resolve('process/browser'),
                tty: require.resolve('tty-browserify'),
                url: require.resolve('url/'),
                http: require.resolve('stream-http'),
                https: require.resolve('https-browserify'),
                zlib: require.resolve('browserify-zlib'),
                vm: require.resolve('vm-browserify'),
                child_process: false,
                async_hooks: false,
                perf_hooks: false,
                v8: false,
                readline: false,
                module: false,
              },
            },
            plugins: [
              new webpack.ProvidePlugin({
                Buffer: ['buffer', 'Buffer'],
                process: 'process/browser',
              }),
              // Plugin to handle node: protocol imports
              new webpack.NormalModuleReplacementPlugin(/^node:/, (resource) => {
                const mod = resource.request.replace(/^node:/, '');
                const nodeModuleMap = {
                  path: 'path-browserify',
                  os: 'os-browserify/browser',
                  crypto: 'crypto-browserify',
                  stream: 'stream-browserify',
                  util: 'util/',
                  url: 'url/',
                  buffer: 'buffer/',
                  assert: 'assert/',
                  http: 'stream-http',
                  https: 'https-browserify',
                  zlib: 'browserify-zlib',
                  vm: 'vm-browserify',
                  constants: 'constants-browserify',
                  process: 'process/browser',
                  tty: 'tty-browserify',
                };

                if (nodeModuleMap[mod]) {
                  resource.request = nodeModuleMap[mod];
                }
              }),
            ],
          };
        },
      };
    },
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

  themeConfig: {
    image: 'img/physical-ai-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Humanoid Robotics Book',
        src: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMzOGJkZjgiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cmVjdCB4PSI0IiB5PSI0IiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHJ4PSIzIi8+PGNpcmNsZSBjeD0iOSIgY3k9IjEwIiByPSIxIi8+PGNpcmNsZSBjeD0iMTUiIGN5PSIxMCIgcj0iMSIvPjxwYXRoIGQ9Ik05IDE1aDZlIi8+PHBhdGggZD0iTTEyIDJ2MiIvPjwvc3ZnPg==',
        srcDark: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMzOGJkZjgiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2tlLWxpbmVjYXA9InJvdW5kIj48cmVjdCB4PSI0IiB5PSI0IiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHJ4PSIzIi8+PGNpcmNsZSBjeD0iOSIgY3k9IjEwIiByPSIxIi8+PGNpcmNsZSBjeD0iMTUiIGN5PSIxMCIgcj0iMSIvPjxwYXRoIGQ9Ik05IDE1aDZlIi8+PHBhdGggZD0iTTEyIDJ2MiIvPjwvc3ZnPg==',
        width: 28,
        height: 28,
      },      
      hideOnScroll: false,
      items: [
        {
          type: 'doc',
          docId: 'module_0/module_0_overview',
          label: 'Modules',
          position: 'left'
        },
        {
          type: 'search',
          position: 'left',
        },
        {
          href: 'https://github.com/physical-ai-humanoid-robotics/physical-ai-humanoid-robotics',
          position: 'right',
          className: 'navbar-github-link',
          'aria-label': 'GitHub repository',
          html: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>',
        },
        {
          to: '/login',
          label: 'Login',
          position: 'right',
          className: 'navbar-login-btn',
        },
        {
          to: '/register',
          label: 'Sign Up',
          position: 'right',
          className: 'navbar-signup-btn',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Physical AI Logo',
        src: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMzOGJkZjgiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cmVjdCB4PSI0IiB5PSI0IiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHJ4PSIzIi8+PGNpcmNsZSBjeD0iOSIgY3k9IjEwIiByPSIxIi8+PGNpcmNsZSBjeD0iMTUiIGN5PSIxMCIgcj0iMSIvPjxwYXRoIGQ9Ik05IDE1aDZlIi8+PHBhdGggZD0iTTEyIDJ2MiIvPjwvc3ZnPg==',
        width: 40,
        height: 40,
      },
      links: [
        {
          title: 'Textbook Modules',
          items: [
            {
              label: 'Module 0 — Overview',
              to: '/module_0/module_0_overview'
            },
            {
              label: 'Module 1 — ROS 2 Fundamentals',
              to: '/docs/module_1/module_1_0'
            },
            {
              label: 'Module 2 — Gazebo Simulation',
              to: '/docs/module_2/module_2_0'
            },
            {
              label: 'Module 3 — Isaac Sim Basics',
              to: '/docs/module_3/module_3_0'
            },
            {
              label: 'Module 4 — VLA Voice to Action',
              to: '/docs/module_4/module_4_0'
            }
          ]
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/physical-ai-humanoid-robotics/physical-ai-humanoid-robotics'
            },
            {
              label: 'ROS Documentation',
              href: 'https://docs.ros.org/'
            },
            {
              label: 'Isaac Sim Documentation',
              href: 'https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html'
            },
            {
              label: 'Gazebo Simulation',
              href: 'https://gazebosim.org/'
            }
          ]
        },
        {
          title: 'Learning',
          items: [
            {
              label: 'Exercises & Labs',
              to: '/docs/module_1/module_1_lab'
            },
            {
              label: 'Capstone Projects',
              to: '/docs/module_4/capstone_autonomous_humanoid'
            },
            {
              label: 'FAQ',
              to: '/docs/module_0/module_0_overview#frequently-asked-questions'
            },
            {
              label: 'Glossary',
              to: '/docs/module_0/module_0_overview#glossary'
            }
          ]
        }
      ],
      copyright: `© ${new Date().getFullYear()} Physical AI & Humanoid Robotics — Authored by Areeba | Empowering the Future of Robotics`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml', 'docker', 'cpp', 'csharp', 'typescript'],
    },
  } satisfies Preset.ThemeConfig,
};

// Note: For development server proxy configuration,
// you would typically handle this in your start script or with a separate proxy

export default config;
