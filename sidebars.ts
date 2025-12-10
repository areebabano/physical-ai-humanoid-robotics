import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  textbookSidebar: [
    {
      type: 'category',
      label: 'Module 0 – Overview',
      items: [
        'module_0/module_0_overview',
      ]
    },
    {
      type: 'category',
      label: 'Module 1 – The Robotic Nervous System',
      items: [
        'module_1/module_1_0',
        'module_1/module_1_1',
        'module_1/module_1_2',
        'module_1/module_1_3',
        'module_1/module_1_4',
        'module_1/module_1_5',
        'module_1/module_1_lab'
      ]
    },
    {
      type: 'category',
      label: 'Module 2 – The Digital Twin',
      items: [
        'module_2/module_2_0',
        'module_2/module_2_1',
        'module_2/module_2_2',
        'module_2/module_2_3',
        'module_2/module_2_4',
        'module_2/module_2_5',
        'module_2/module_2_lab'
      ]
    },
    {
      type: 'category',
      label: 'Module 3 – The AI-Robot Brain',
      items: [
        'module_3/module_3_0',
        'module_3/module_3_1',
        'module_3/module_3_2',
        'module_3/module_3_3',
        'module_3/module_3_4',
        'module_3/module_3_5',
        'module_3/module_3_lab'
      ]
    },
    {
      type: 'category',
      label: 'Module 4 – Vision-Language-Action',
      items: [
        'module_4/module_4_0',
        'module_4/module_4_1',
        'module_4/module_4_2',
        'module_4/module_4_3',
        'module_4/module_4_4',
        'module_4/module_4_lab'
      ]
    }
  ]
};

export default sidebars;
