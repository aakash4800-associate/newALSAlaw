import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const practiceAreas = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/practice-areas" }),
  schema: z.object({
    title: z.string(),
    icon: z.string(),
    summary: z.string(),
    order: z.number(),
  }),
});

const attorneys = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/attorneys" }),
  schema: z.object({
    name: z.string(),
    title: z.string(),
    practice: z.string(),
    initials: z.string(),
    order: z.number(),
    image: z.string().optional(),
    tagline: z.string().optional(),
  }),
});

const testimonials = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/testimonials" }),
  schema: z.object({
    author: z.string(),
    role: z.string(),
    order: z.number(),
  }),
});

export const collections = { practiceAreas, attorneys, testimonials };
