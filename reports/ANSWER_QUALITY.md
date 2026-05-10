# End-to-End RAG Answer Quality
<!-- style: v2, 2026-05-05 -->

All crawlers produce similar LLM answer quality (4.03-4.40 out of 5). crawl4ai leads slightly at 4.40; markcrawl ranks 7th at 4.03 — a 8.3% gap from the best. The gaps are small but consistent.

> **Single-trial measurement.** Each per-site number reported here comes from one benchmark run. Network jitter, WAF state, and server load can shift per-site speed and coverage between runs by single-digit percent. Confidence intervals reflect query-set sampling only — not run-to-run variance. Multi-trial validation is v1.5 work; see [METHODOLOGY.md](METHODOLOGY.md#single-trial-measurement).

**Run:** `run_v13_merged_20260504_203748` | **Started:** 2026-05-04T13:36:42Z | **Ended:** 2026-05-05T05:41:25.381501+00:00 | **Pool:** 1.2 (sha256:caa35)

**Tool versions in this run:**

| Tool | Version | Status |
|---|---|---|
| colly+md | go binary | available |
| crawl4ai | 0.8.6 | available |
| crawl4ai-raw | go binary | available |
| crawlee | 1.6.2 | available |
| firecrawl | — | skipped: FIRECRAWL_API_KEY not set |
| markcrawl | 0.10.5 | available |
| playwright | 1.58.0 | available |
| scrapy+md | 2.15.0 | available |


Each tool's crawled content is chunked, embedded, retrieved (top-10),
and sent to `gpt-4o-mini` to generate an answer. Answers are scored by
`gpt-4o-mini` on correctness, relevance, completeness, and usefulness (1-5 each).

**Scoring scale:** 1 = wrong/irrelevant, 2 = partially relevant, 3 = acceptable, 4 = good, 5 = excellent/complete. Scores are averaged across all queries per tool. An overall score above 4.0 indicates consistently good answers.

## Summary (104 queries across 11 sites)

| Tool | Correctness | Relevance | Completeness | Usefulness | **Overall** | Avg tokens/query |
|---|---|---|---|---|---|---|
| crawl4ai | 4.53 | 4.47 | 4.21 | 4.39 | **4.40 ±0.23** | 4,275 |
| crawl4ai-raw | 4.51 | 4.41 | 4.13 | 4.33 | **4.35 ±0.23** | 4,204 |
| crawlee | 4.50 | 4.35 | 4.08 | 4.31 | **4.31 ±0.24** | 3,600 |
| colly+md | 4.45 | 4.32 | 4.04 | 4.25 | **4.27 ±0.25** | 3,683 |
| scrapy+md | 4.41 | 4.17 | 3.84 | 4.09 | **4.13 ±0.26** | 4,180 |
| playwright | 4.38 | 4.18 | 3.82 | 4.09 | **4.12 ±0.24** | 3,536 |
| markcrawl | 4.33 | 4.06 | 3.73 | 4.01 | **4.03 ±0.27** | 4,122 |

> **Column definitions:** All scores are 1-5 averages across queries, judged by `gpt-4o-mini`. **Correctness** = factual accuracy. **Relevance** = answers the question asked. **Completeness** = covers all aspects. **Usefulness** = practical value to the user. **Overall** = mean of the four dimensions (± 95% confidence interval). **Avg tokens/query** = estimated input tokens per query (chunk words x 1.33). Gaps within the ± range are not statistically significant.

## What this means in practice

The quality gap between the best (crawl4ai, 4.40) and worst (markcrawl, 4.03) crawler is 0.36 points on a 5-point scale -- 8.3% relative. This gap is real but small.

For most use cases, your choice of crawler will not noticeably affect the quality of LLM-generated answers. All tools produce answers that score above 4.0 ("good") on average, meaning users get helpful, accurate responses regardless of which crawler feeds the pipeline.

**Executive takeaway:** Switching crawlers purely to improve answer quality is unlikely to justify the migration effort. The cost and speed differences between tools are far more impactful on your bottom line -- see [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar-level analysis.

## react-dev

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawl4ai-raw | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| scrapy+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawlee | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| colly+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| playwright | 4.88 | 4.81 | 4.75 | 4.81 | 4.81 ±0.37 |
| markcrawl | 4.62 | 4.44 | 4.25 | 4.44 | 4.44 ±0.59 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for react-dev</summary>

**Q1: How do I manage state in a React component?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, follow these steps:  1. **Identify** the different visual stat... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, you can follow these steps:  1. **Identify your component’s di... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, you can follow these steps:  1. **Identify your component’s di... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, follow these steps:  1. **Identify** the different visual stat... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, follow these steps:  1. **Identify** the different visual stat... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, follow these steps:  1. **Identify** the different visual stat... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To manage state in a React component, follow these steps:  1. **Identify** the different visual stat... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How does the useEffect hook work in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It is c... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `useEffect` hook in React allows you to synchronize a component with an external system. It take... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do I create and use context in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the Context**: Use `createConte... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To create and use context in React, follow these steps:  1. **Create the context**: Use `createConte... |

**Q4: What is JSX and how does React use it?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows you to write HTML-like markup inside a JavaScri... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within a J... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within a J... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | JSX is a syntax extension for JavaScript that allows developers to write HTML-like markup within Jav... |

**Q5: How do I render lists and use keys in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the `map()` function to transform an array of data into an arr... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use the JavaScript `map()` function to transform an array of data ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To render lists in React, you can use JavaScript's `map()` function to transform an array of data in... |

**Q6: How do I use the useRef hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. **Import the Hook**: Start by importing `... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. **Import the Hook**: Start by importing `... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. **Import the Hook**: Start by importing `... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useRef` hook in React, follow these steps:  1. Import the `useRef` hook from React:    `... |

**Q7: How do I pass props between React components?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can pass props between React components by adding them to the JSX of the child component when it... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can pass props between React components by adding them to the JSX of the child component when yo... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can pass props between React components by adding them to the JSX of the child component when yo... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can pass props between React components by including them in the JSX of the parent component whe... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To pass props between React components, you add them to the JSX of the child component when renderin... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To pass props between React components, you can follow these steps:  1. **Pass props to the child co... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To pass props between React components, you add them to the JSX of the child component when renderin... |

**Q8: How do I conditionally render content in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In React, you can conditionally render content using JavaScript syntax such as `if` statements, the ... |

**Q9: What is the useMemo hook for in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to create and memoize a value from a function call, re-running t... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `useMemo` hook in React is used to cache the result of a calculation between re-renders, allowin... |

**Q10: How do I use the useState hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. Import `useState` from React at the top... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. Import `useState` from React at the top... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. Import `useState` from React at the top... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. **Import the Hook**: At the top of your... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. **Import the Hook**: At the top of your... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. Import `useState` from React at the top... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useState` hook in React, follow these steps:  1. **Import the Hook**: At the top of your... |

**Q11: How do I use the useCallback hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you wrap the function you want to cache between re-renders w... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you need to wrap the function you want to cache with `useCal... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, follow these steps:  1. **Import the Hook**: First, import `... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, follow these steps:  1. **Import the Hook**: Start by import... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, you can follow this pattern:  1. Import `useCallback` from R... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useCallback` hook in React, follow these steps:  1. **Import the Hook**: Start by import... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q12: How do I use the useReducer hook in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Start by importi... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Start by importi... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the hook**: Start by importi... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Import `useReduc... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Start by importi... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Start by importi... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the `useReducer` hook in React, follow these steps:  1. **Import the Hook**: Start by importi... |

**Q13: How do I handle events like clicks in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In React, you handle events like clicks by defining event handler functions inside your components a... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In React, you handle events like clicks by defining an event handler function inside your component ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to define an event handler function inside your comp... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In React, you handle events like clicks by defining an event handler function inside your component ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you define an event handler function inside your component an... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to define an event handler function inside your comp... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle events like clicks in React, you need to define an event handler function inside your comp... |

**Q14: What is the Suspense component in React?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to display a fallback UI (such as a loading spinner) whil... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Suspense component in React allows you to display a fallback UI (such as a loading spinner) whil... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The `<Suspense>` component in React allows you to display a fallback UI (such as a loading spinner) ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `<Suspense>` component in React allows you to display a fallback UI (such as a loading spinner) ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The `<Suspense>` component in React allows you to display a fallback UI while its children are loadi... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `<Suspense>` component in React allows you to display a fallback UI (such as a loading spinner) ... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q15: How do I add interactivity to React components?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can use event handlers. Define a function that handles... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can use event handlers. React allows you to attach you... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can use event handlers. React allows you to attach you... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can use event handlers. Define a function that handles... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can add interactivity to React components by using event handlers. React allows you to attach yo... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can define event handlers as functions within your com... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To add interactivity to React components, you can use event handlers. Define a function that will be... |

**Q16: How do I install and set up a new React project?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install a build tool**: Choose ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, you should follow these steps:  1. **Choose a React-power... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, you should start by choosing a React-powered framework po... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install a build tool** like Vit... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install Node.js**: Ensure you h... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To install and set up a new React project, follow these steps:  1. **Install a build tool**: Use a b... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## stripe-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai-raw | 4.67 | 4.50 | 4.44 | 4.50 | 4.53 ±0.50 |
| crawl4ai | 4.67 | 4.50 | 4.33 | 4.50 | 4.50 ±0.53 |
| scrapy+md | 4.56 | 4.39 | 4.22 | 4.33 | 4.38 ±0.54 |
| playwright | 4.56 | 4.39 | 4.06 | 4.33 | 4.33 ±0.56 |
| crawlee | 4.56 | 4.33 | 4.00 | 4.33 | 4.31 ±0.59 |
| markcrawl | 4.33 | 4.06 | 3.78 | 4.00 | 4.04 ±0.65 |
| colly+md | 4.22 | 3.89 | 3.50 | 3.83 | 3.86 ±0.68 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for stripe-docs</summary>

**Q1: How do I create a payment intent with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you need to perform the following steps on your server:  1. U... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ```bash curl https:/... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ```bash curl https:/... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | To create a payment intent with Stripe, you can use the following cURL command:  ```bash curl https:... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ``` curl https://api... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | To create a PaymentIntent with Stripe, you can use the following cURL command:  ``` curl https://api... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I handle webhooks from Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint on your server that can accept P... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint on your server that can receive ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint on your server that can receive ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint on your server that can accept P... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint in your application that can rec... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint that can receive events from Str... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To handle webhooks from Stripe, you need to set up an HTTP endpoint in your application that can rec... |

**Q3: How do I set up Stripe subscriptions?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up Stripe subscriptions, follow these steps:  1. **Create Products and Prices**: Use the Prod... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: How do I authenticate with the Stripe API?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you need to use your account’s API keys. Include a valid key in... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you need to use your account’s API keys. Include a valid key in... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To authenticate with the Stripe API, you must include an API secret key in every API call. After cre... |
| colly+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: How do I handle errors in the Stripe API?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. **Notify the Customer**: Inform the customer tha... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should check the HTTP response codes and the error type retu... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should check the HTTP response codes and the error type retu... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, you should:  1. **Understand Error Types**: Errors fall into thr... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To handle errors in the Stripe API, ensure your code is defensive by managing all possible error typ... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | To handle errors in the Stripe API, you can check if the response contains an error. If it does, dis... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | To handle errors in the Stripe API, you can check if the response contains an error. If it does, dis... |

**Q6: How do I process refunds with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can follow these steps:  1. **Using the Dashboard**:    - Naviga... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Refunds API or the Dashboard. Here are the steps:  1... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Refunds API or the Dashboard. Here are the steps:  1... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can process refunds with Stripe using either the Refunds API or the Dashboard. Here’s how:  ### ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Refunds API or the Dashboard. Here are the steps:  1... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can process refunds with Stripe using either the Refunds API or the Dashboard. To issue a refund... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To process refunds with Stripe, you can use the Refunds API or the Dashboard. Here are the steps:  1... |

**Q7: How do I use Stripe checkout for payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Set Up Your Server**: Create an endpo... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Create a Stripe Account**: Register f... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, follow these steps:  1. **Create a Stripe Account**: Register f... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you can follow these steps:  1. **Create a Checkout Session**: ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you need to create a Checkout Session by setting up an endpoint... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use Stripe Checkout for payments, you need to create a Checkout Session by setting up an endpoint... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I test Stripe payments in development?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, follow these steps:  1. Ensure that `stripe listen` is runni... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. **Set Up a Sandbox**: C... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. **Set Up a Sandbox**: C... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use Sandboxes to simulate live mode and create test ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following methods:  1. **Set up a sandbox**:... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. **Set Up a Sandbox**: C... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To test Stripe payments in development, you can use the following steps:  1. **Set Up a Sandbox**: C... |

**Q9: What are Stripe Connect and platform payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows businesses to build platforms or marketplaces that manage pa... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows businesses to build platforms or marketplaces that manage pa... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows platforms and marketplaces to facilitate payments and pay ou... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows businesses to build platforms or marketplaces that manage pa... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows businesses to build platforms or marketplaces that manage pa... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Stripe Connect is a service that allows businesses to build platforms or marketplaces that manage pa... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q10: How do I set up usage-based billing with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai-raw | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q11: How do I manage Stripe API keys?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Store Securely**: Use secrets manageme... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Store Securely**: Use secrets manageme... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, you can find them in the Stripe dashboard. If you cannot view your API ke... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Store securely**: Use a secrets vault ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Store securely**: Use a secrets vault ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To manage Stripe API keys, follow these best practices:  1. **Store securely**: Use a secrets vault ... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q12: How do I handle Stripe rate limits?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai-raw | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q13: How do I use metadata with Stripe objects?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by adding it to most requests, such as processing charges o... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use metadata to attach key-value data to Stripe objects, such as Account, Charge, Customer, ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects to attach key-value data that is meaningful to your busines... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by attaching key-value pairs to them. This allows you to st... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects by adding it to common requests, such as processing payment... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can use metadata with Stripe objects to attach key-value data, allowing you to store additional,... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can use metadata to attach key-value data to Stripe objects, such as Account, Charge, Customer, ... |

**Q14: How do I set up Apple Pay with Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, ensure that Apple Pay is enabled for Checkout in your Stripe Dashbo... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Register for an Apple Merchant ID**: Obta... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To set up Apple Pay with Stripe, follow these steps:  1. **Set up Stripe**: Create a Stripe account.... |

**Q15: How do I issue cards with Stripe Issuing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, follow these steps:  1. **Enable the account to use Issuing**: A... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, follow these steps:  1. **Enable the account to use Issuing**: A... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you need to follow these steps:  1. **Enable the account to use ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you need to follow these steps:  1. **Create a cardholder**: Ref... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To issue cards with Stripe Issuing, you need to follow these steps:  1. **Enable the account to use ... |
| markcrawl | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q16: How do I recover failed subscription payments?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can enable automatic retries for failed balance payment... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can use Stripe's revenue recovery features, which inclu... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can use Stripe's revenue recovery features, which inclu... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Stripe provides automated recovery features to help collect payments that might have been unsuccessf... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you should set up a webhook endpoint to listen for the `cus... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you can set up webhooks to receive notifications about paym... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To recover failed subscription payments, you should set up a webhook endpoint to listen for the `cus... |

**Q17: How does Stripe handle tax calculation for billing?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by using the Stripe Tax APIs to automatically calculate s... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Stripe calculates tax for billing based on the customer's address. For new customers, it uses the bi... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Stripe calculates tax for billing based on the customer's address. For new customers, it uses the bi... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing through its Stripe Tax feature, which automatically calcu... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Stripe allows you to calculate tax in various ways during the billing process. You can show a tax es... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Stripe handles tax calculation for billing by allowing you to choose when and how often to calculate... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Stripe allows you to calculate tax in various ways during the billing process. You can show a tax es... |

**Q18: How do I migrate data to Stripe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, you can either request a data migration with Stripe or manually migrate b... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. **Understand the Migration Process**: Review Stri... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. **Understand the Migration Process**: Review Stri... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. **Create a Migration Plan**: Outline a timeline a... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. Understand the Stripe migration process and scope... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To migrate data to Stripe, follow these steps:  1. Understand the Stripe migration process and scope... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## huggingface-transformers

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| scrapy+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| markcrawl | 4.88 | 5.00 | 4.75 | 4.88 | 4.88 ±0.24 |
| crawlee | 4.62 | 4.62 | 4.38 | 4.50 | 4.53 ±0.66 |
| playwright | 4.50 | 4.25 | 3.88 | 4.25 | 4.22 ±0.95 |
| crawl4ai-raw | 4.25 | 4.00 | 3.25 | 3.88 | 3.84 ±0.97 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for huggingface-transformers</summary>

**Q1: How do I use the Pipeline class for inference in Transformers?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. Import the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. Import the ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. **Import th... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. Import the ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To use the Pipeline class for inference in Transformers, you can follow these steps:  1. Import the ... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I train a model with the Hugging Face Trainer?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To train a model with the Hugging Face Trainer, follow these steps:  1. **Prepare Your Model and Dat... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To train a model with the Hugging Face Trainer, you need to follow these steps:  1. **Prepare your m... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To train a model with the Hugging Face Trainer, follow these steps:  1. Load a model and tokenizer: ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To train a model with the Hugging Face Trainer, you can use the following code snippet:  ```python f... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do I generate text with a large language model?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To generate text with a large language model, you can use the `generate()` API provided in the Trans... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To generate text with a large language model (LLM) using the Transformers library, you can follow th... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To generate text with a large language model, you can use the `pipeline` function from the `transfor... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To generate text with a large language model, you can use the Pipeline class from the Transformers l... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q4: What are the design principles behind the Transformers library?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The design principles behind the Transformers library include:  1. **Composition over Abstraction**:... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The design principles behind the Transformers library are:  1. **Fast and easy to use**: Every model... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | The design principles behind the Transformers library are: 1. Fast and easy to use: Every model is i... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | The design principles behind the Transformers library are:  1. Fast and easy to use: Every model is ... |
| playwright | 5 | 5 | 4 | 5 | 4.8 | The design principles behind the Transformers library are:  1. **Fast and easy to use**: Every model... |

**Q5: What models are supported in the Transformers library?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Transformers library supports a wide range of models, including but not limited to:  - Text mode... |
| markcrawl | 4 | 5 | 3 | 4 | 4.0 | The Transformers library supports state-of-the-art machine learning models in text, computer vision,... |
| crawlee | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: What is the Pipeline API reference in Transformers?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Pipeline API in Transformers is a simple but powerful inference API that allows users to perform... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Pipeline API in Transformers is a simple but powerful inference API that allows users to easily ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Pipeline API reference in Transformers provides a complete list of available tasks that can be p... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | The Pipeline API in Transformers is a simple and optimized inference class for various machine learn... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What does the Trainer class support for distributed training?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Trainer class supports distributed training on multiple GPUs/TPUs.... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Trainer class supports distributed training on multiple GPUs/TPUs and mixed precision for NVIDIA... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Trainer class supports distributed training with PEFT adapters out of the box. It passes `exclud... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | The Trainer class supports features such as mixed precision, torch.compile, and FlashAttention for d... |
| crawlee | 4 | 5 | 4 | 4 | 4.2 | The Trainer class supports features such as mixed precision, torch.compile, and FlashAttention for t... |

**Q8: What is the Hugging Face Transformers library?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The Hugging Face Transformers library acts as the model-definition framework for state-of-the-art ma... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The Hugging Face Transformers library is a model-definition framework for state-of-the-art machine l... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The Hugging Face Transformers library is a model-definition framework for state-of-the-art machine l... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The Hugging Face Transformers library is a model-definition framework for state-of-the-art machine l... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The Hugging Face Transformers library is a model-definition framework for state-of-the-art machine l... |

</details>

## kubernetes-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawl4ai-raw | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| scrapy+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawlee | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| colly+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| playwright | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| markcrawl | 4.75 | 4.62 | 4.50 | 4.62 | 4.62 ±0.73 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for kubernetes-docs</summary>

**Q1: What is a Kubernetes pod and what does it represent?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit in Kubernetes, representing a group of one or more ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes pod is the smallest deployable unit of computing that you can create and manage in Kube... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do Kubernetes Deployments manage replicas and rollouts?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by using a Deployment Controller that changes th... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by providing declarative updates for Pods and Re... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by providing declarative updates for Pods and Re... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by creating and controlling ReplicaSets. When a ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by providing declarative updates for Pods and Re... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by providing declarative updates for Pods and Re... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Deployments manage replicas and rollouts by providing declarative updates for Pods and Re... |

**Q3: What is a Kubernetes Service and how does it expose pods?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes an application running on a set of Pods over a n... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes an application running in a cluster behind a sin... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes an application running in a cluster behind a sin... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that defines a logical set of Pods and a policy for accessing... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running as one or more Pod... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running as one or more Pod... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A Kubernetes Service is an abstraction that exposes a network application running as one or more Pod... |

**Q4: How do I use ConfigMaps to inject configuration into pods?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods in four different ways:  1. **Inside a cont... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods in several ways:  1. **As Environment Varia... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods in several ways:  1. **As Environment Varia... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To use ConfigMaps to inject configuration into pods, follow these steps:  1. **Create a ConfigMap** ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these methods:  1. **As Enviro... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these methods:  1. **As Enviro... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can use ConfigMaps to inject configuration into pods by following these methods:  1. **As Enviro... |

**Q5: How do I manage Secrets in Kubernetes?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To manage Secrets in Kubernetes, you can use the `kubectl` command-line tool to create, edit, and de... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To manage Secrets in Kubernetes, you can use the `kubectl` command-line tool to create, edit, and de... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To manage Secrets in Kubernetes, follow these guidelines:  1. **Create Secrets**: Use `kubectl`, con... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool. Here are the steps:  1. ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool. Here are the steps:  1. ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | You can manage Secrets in Kubernetes using the `kubectl` command-line tool. Here are the steps:  1. ... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: What are namespaces in Kubernetes and when should I use them?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Namespaces in Kubernetes provide a mechanism for isolating groups of resources within a single clust... |

**Q7: How does Kubernetes Ingress route external traffic?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Kubernetes Ingress routes external traffic by exposing HTTP and HTTPS routes from outside the cluste... |

**Q8: What is a StatefulSet and when do I need one?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications in Kubernetes. It runs a... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a Kubernetes workload API object used to manage stateful applications. It runs a gr... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a Kubernetes workload API object used to manage stateful applications. It runs a gr... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object used to manage stateful applications in Kubernetes. It runs a... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a Kubernetes workload API object used to manage stateful applications. It runs a gr... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a Kubernetes workload API object used to manage stateful applications. It runs a gr... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A StatefulSet is a workload API object in Kubernetes used to manage stateful applications. It runs a... |

</details>

## postgres-docs

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| scrapy+md | 4.25 | 3.88 | 3.38 | 3.88 | 3.84 ±1.06 |
| crawl4ai-raw | 4.00 | 3.62 | 3.12 | 3.50 | 3.56 ±1.07 |
| markcrawl | 4.00 | 3.50 | 3.00 | 3.50 | 3.50 ±1.11 |
| crawl4ai | 4.00 | 3.50 | 3.00 | 3.50 | 3.50 ±1.11 |
| playwright | 3.75 | 3.25 | 2.62 | 3.12 | 3.19 ±1.05 |
| crawlee | 3.75 | 3.12 | 2.50 | 3.12 | 3.12 ±1.08 |
| colly+md | 3.75 | 3.12 | 2.50 | 3.12 | 3.12 ±1.08 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for postgres-docs</summary>

**Q1: What data types does PostgreSQL support?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a variety of data types, including:  1. **Base Types**:     - Integer    - Numer... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a rich set of native data types, including:  - Primitives: Integer, Numeric, Str... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports a rich set of native data types, including:  - Primitives: Integer, Numeric, Str... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports the following data types:  1. **Numeric Types**    - Integer Types    - Arbitrar... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports the following data types:  1. **Numeric Types**    - Integer Types    - Arbitrar... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL supports the following data types:  1. **Numeric Types**    - Integer Types    - Arbitrar... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | PostgreSQL supports the following data types:  1. **timestamp [ (p) ] [ without time zone ]** - 8 by... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What is the SQL syntax for queries in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The SQL syntax for queries in PostgreSQL is as follows:  ``` SELECT [ ALL \| DISTINCT [ ON ( expressi... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do indexes work in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL are secondary indexes, meaning they are stored separately from the table's mai... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL are secondary indexes that are physically separate from the table they describ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL are secondary indexes that are physically separate from the table they describ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL enhance database performance by allowing the database server to find and retri... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL enhance database performance by allowing the database server to find and retri... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Indexes in PostgreSQL enhance database performance by allowing the database server to find and retri... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: How does MVCC concurrency control work in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | MVCC (Multiversion Concurrency Control) in PostgreSQL allows multiple transactions to access the dat... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Multi-version concurrency control (MVCC) in PostgreSQL allows multiple transactions to read and writ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Multi-version concurrency control (MVCC) in PostgreSQL allows multiple transactions to read and writ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL uses a multiversion model (Multiversion Concurrency Control, MVCC) for concurrency contro... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: How do transactions work in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In PostgreSQL, transactions are a combination of commands that must act as a single atomic unit, mea... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Transactions in PostgreSQL are initiated using the `BEGIN` command, which starts a transaction block... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How do I set up logical replication in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What built-in functions and operators are available in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL provides a large number of built-in functions and operators for various data types, inclu... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL provides a large number of built-in functions and operators for various data types, inclu... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL provides a large number of built-in functions and operators, including:  1. Logical Opera... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL provides a large number of built-in functions and operators for various data types, inclu... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL provides a large number of built-in functions and operators for various data types, as de... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | PostgreSQL provides a large number of built-in functions and operators for various data types, inclu... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I use full text search in PostgreSQL?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## mdn-css

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.75 | 4.75 | 4.62 | 4.62 | 4.69 ±0.61 |
| crawl4ai-raw | 4.75 | 4.75 | 4.62 | 4.62 | 4.69 ±0.61 |
| crawlee | 4.75 | 4.62 | 4.50 | 4.62 | 4.62 ±0.73 |
| colly+md | 4.75 | 4.62 | 4.50 | 4.62 | 4.62 ±0.73 |
| playwright | 4.50 | 4.25 | 4.00 | 4.25 | 4.25 ±0.96 |
| markcrawl | 3.75 | 3.25 | 2.75 | 3.12 | 3.22 ±1.03 |
| scrapy+md | 3.00 | 2.12 | 1.12 | 2.00 | 2.06 ±0.12 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for mdn-css</summary>

**Q1: How does the CSS display property work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The CSS `display` property defines how a box and any boxes inside it behave. It determines the outer... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The CSS `display` property defines how a box and any boxes inside it behave. It establishes the oute... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The CSS `display` property determines how an element is rendered on the page, affecting its outer an... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The CSS `display` property determines how an element is displayed on the web page. It can switch ele... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The CSS `display` property determines how an element is displayed on the web page, defining its oute... |
| scrapy+md | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do I use flexbox for page layout?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How does CSS Grid layout work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout introduces a two-dimensional grid system to CSS, allowing for the layout of major pa... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout introduces a two-dimensional grid system to CSS, allowing elements to be placed with... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout introduces a two-dimensional grid system to CSS, allowing elements to be placed with... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by creating a two-dimensional grid system defined by intersecting horizontal a... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by creating a grid container using the `display: grid` or `display: inline-gri... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | CSS Grid layout works by creating a two-dimensional grid system defined by intersecting horizontal a... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What is the CSS box model?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a fundamental concept in CSS that represents each element as a rectangular box.... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a fundamental concept in CSS that defines how elements are laid out on a webpag... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a fundamental concept in CSS that defines how elements are laid out on a webpag... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a fundamental concept in CSS that defines how every visible element on a webpag... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a fundamental concept in CSS that defines how elements are structured and displ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The CSS box model is a fundamental concept in CSS that defines how every visible element on a webpag... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: How does the CSS margin property work?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property defines the space around an element's border, creating a margin area that se... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property defines the space around an element's border, creating a margin area that se... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property defines the space around an element's border, creating a margin area that se... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property defines the space around an element's border. It can be set using shorthand ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The CSS margin property defines the space around an element, creating a margin area that separates i... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How does CSS specificity determine which rules win?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of a CSS selector based on the ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of a CSS selector based on the ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating the weight of a CSS selector based on the ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by calculating a weight based on the number of selectors ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | CSS specificity determines which rules win by comparing the specificity values of competing selector... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: How does the :hover pseudo-class work in CSS?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS is used to style an element when a user's pointer hovers over it. F... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS is used to style an element when a user's pointer hovers over it. I... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS is used to style an element when a user's pointer hovers over it. I... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS is used to apply styles to an element when a user's pointer hovers ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS is used to apply styles to an element when a user's pointer hovers ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The `:hover` pseudo-class in CSS is used to apply styles to an element when the user's pointer hover... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q8: How do I create CSS animations?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To create CSS animations, you need to define two main components: a style describing the CSS animati... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To create CSS animations, you need to define two main components: a style describing the CSS animati... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To create CSS animations, you need to define a style describing the animation and a set of keyframes... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To create CSS animations, you can use the `@keyframes` rule to define the animation's behavior and t... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

</details>

## rust-book

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| markcrawl | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawl4ai | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawl4ai-raw | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| scrapy+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| crawlee | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| colly+md | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |
| playwright | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for rust-book</summary>

**Q1: What is ownership in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a feature that ensures each value has a single owner at any given time, which h... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a feature that ensures each value has a single owner at any given time, which h... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Ownership in Rust is a set of rules that govern how a Rust program manages memory. Each value in Rus... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: How do references and borrowing work in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to borrow a value without taking ownership of it. When you create a re... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to refer to a value without taking ownership of it. The syntax `&s1` c... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to refer to a value without taking ownership of it. The syntax `&s1` c... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to borrow values without taking ownership. There are two types of refe... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Rust, references and borrowing allow functions to access data without taking ownership. When a fu... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, references allow you to borrow values without taking ownership. When you create a reference... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In Rust, references and borrowing allow functions to access data without taking ownership. When a fu... |

**Q3: How do I define structs in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the keyword `struct` followed by the name of the struct. Inside ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct and then... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct and then... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct. Inside ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct. Inside ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct. Inside ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | To define a struct in Rust, you use the `struct` keyword followed by the name of the struct. Inside ... |

**Q4: How do enums work in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. Each variant can hold... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. They enable you to ex... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. They enable you to ex... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. Each variant can hold... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. They are useful for e... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. Each variant can hold... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Enums in Rust allow you to define a type by enumerating its possible variants. They are useful for e... |

**Q5: How do I use generics in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | In Rust, you can use generics by defining types, functions, and methods with abstract stand-ins for ... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To use generics in Rust, you define a type parameter in angle brackets (`<>`) after the name of a st... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To use generics in Rust, you can define your own types, functions, and methods with generic type par... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, you can use generics by defining functions, structs, enums, and methods with abstract type ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Rust, you can use generics by defining type parameters in functions, structs, enums, and traits. ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, you can use generics by defining functions, structs, enums, and methods with abstract type ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In Rust, you can use generics by defining type parameters in functions, structs, enums, and traits. ... |

**Q6: What are traits in Rust and how do I define them?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust define the functionality that a particular type has and can share with other types. T... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | In Rust, a _trait_ defines the functionality that a particular type has and can share with other typ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | In Rust, a _trait_ defines the functionality that a particular type has and can share with other typ... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Traits in Rust describe an abstract interface that types can implement. They consist of associated i... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Rust, a *trait* defines the functionality that a particular type has and can share with other typ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | A *trait* in Rust describes an abstract interface that types can implement, consisting of associated... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | A *trait* in Rust defines the functionality a particular type has and can share with other types. It... |

**Q7: How do closures work in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can capture values from their environment in three way... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can capture values from their environment in three way... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can capture values from their surrounding scope. They ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can be saved in variables or passed as arguments to ot... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Closures in Rust are anonymous functions that can capture values from their surrounding scope. They ... |

**Q8: How do I handle errors with Result in Rust?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To handle errors with `Result` in Rust, you can use a `match` expression to differentiate between th... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | To handle errors with `Result` in Rust, you can use a `match` expression to differentiate between th... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | To handle errors with `Result` in Rust, you can use a `match` expression to differentiate between th... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To handle errors with `Result` in Rust, you can use a `match` expression to differentiate between th... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | In Rust, you handle errors using the `Result` enum, which has two variants: `Ok(T)` for success and ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | In Rust, you handle errors using the `Result` type, which has two variants: `Ok(T)` for success and ... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | In Rust, you handle errors using the `Result` enum, which has two variants: `Ok(T)` for success and ... |

</details>

## smittenkitchen

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 3.75 | 3.12 | 2.50 | 3.12 | 3.12 ±1.08 |
| colly+md | 3.50 | 3.12 | 2.38 | 2.75 | 2.94 ±1.02 |
| playwright | 3.38 | 3.12 | 2.25 | 2.88 | 2.91 ±0.94 |
| markcrawl | 3.62 | 2.88 | 2.12 | 2.75 | 2.84 ±0.94 |
| crawl4ai-raw | 3.50 | 2.75 | 2.00 | 2.75 | 2.75 ±0.96 |
| crawlee | 3.00 | 2.88 | 1.88 | 2.50 | 2.56 ±0.75 |
| scrapy+md | 3.38 | 2.50 | 1.75 | 2.50 | 2.53 ±0.73 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for smittenkitchen</summary>

**Q1: How do you make world peace cookies?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 2 | 3 | 2 | 2 | 2.2 | The recipe makes about 16 large cookies, or more if smaller.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What's the recipe for miso chicken and rice?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | **Miso Chicken and Rice Recipe**  * **Servings:** 3 to 4 * **Time:** About 45 minutes, with prep  ##... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q3: How do I make ultimate banana bread?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | To make ultimate banana bread, follow these steps:  1. Preheat your oven to 350 degrees F and butter... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | To make ultimate banana bread, follow this recipe:  1. **Ingredients**:    - 1/2 cup (4 ounces) unsa... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | To make ultimate banana bread, follow this recipe:  1. **Ingredients**:    - 1/2 cup (4 ounces or 11... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What's the skillet-baked macaroni and cheese recipe?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: What vegan recipes are available on Smitten Kitchen?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The vegan recipes available on Smitten Kitchen include:  1. Winter cabbage salad with mandarins and ... |
| colly+md | 3 | 5 | 4 | 4 | 4.0 | The vegan recipes available on Smitten Kitchen are:  - Winter cabbage salad with mandarins and cashe... |
| crawlee | 2 | 5 | 3 | 3 | 3.2 | The vegan recipes available on Smitten Kitchen include:  - Winter cabbage salad with mandarins and c... |
| playwright | 2 | 5 | 3 | 3 | 3.2 | The vegan recipes available on Smitten Kitchen are:  - Winter cabbage salad with mandarins and cashe... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: Show me cookie recipes**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Here are some cookie recipes from the provided context:  1. [Brown Butter Snickerdoodles](https://sm... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Here are some cookie recipes from the provided context:  1. [Brown Butter Snickerdoodles](https://sm... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Here are some cookie recipes from the provided context:  1. Brown Butter Snickerdoodles 2. Brown But... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 1 | 1.8 | I cannot answer this based on the provided context.... |

**Q7: How do you make pumpkin basque cheesecake?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 1 | 1.8 | I cannot answer this based on the provided context.... |

**Q8: What recipes are good for winter?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The following recipes are good for winter:  1. Winter cabbage salad with mandarins and cashews 2. Pu... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The following recipes are good for winter:  1. Winter cabbage salad with mandarins and cashews 2. Pu... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The following recipes are good for winter:  1. Winter cabbage salad with mandarins and cashews 2. Cr... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The context includes several recipes that are suitable for winter, such as:  1. Winter cabbage salad... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | The following recipes are good for winter:  1. Winter cabbage salad with mandarins and cashews 2. Pu... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | The context mentions "Winter" as a season with 81 recipes, indicating that there are recipes suitabl... |
| markcrawl | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |

</details>

## ikea

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| colly+md | 4.62 | 4.38 | 4.12 | 4.38 | 4.38 ±0.82 |
| crawl4ai | 4.12 | 4.50 | 3.75 | 3.88 | 4.06 ±0.92 |
| crawl4ai-raw | 4.12 | 4.38 | 3.62 | 3.88 | 4.00 ±0.98 |
| crawlee | 4.00 | 3.75 | 3.50 | 3.75 | 3.75 ±0.96 |
| scrapy+md | 3.62 | 3.50 | 2.62 | 2.88 | 3.16 ±0.83 |
| playwright | 3.88 | 3.25 | 2.38 | 3.12 | 3.16 ±0.66 |
| markcrawl | 3.75 | 3.12 | 2.50 | 3.12 | 3.12 ±0.81 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for ikea</summary>

**Q1: How much does the MALM bed frame cost at IKEA?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $369.00 at IKEA.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $369.00.... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $249.00 for the Queen size.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The MALM bed frame costs $399.00 for the high bed frame with storage boxes, and $249.00 for the stan... |
| markcrawl | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What's the price of the SLATTUM upholstered bed frame?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 5 | 5 | 5.0 | The price of the SLATTUM upholstered bed frame is $149.00.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The price of the SLATTUM upholstered bed frame is $163.99.... |
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q3: Tell me about the HEMNES 8-drawer dresser**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The HEMNES 8-drawer dresser is available in a white stain finish and measures 63x37 3/4 inches. It i... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The HEMNES 8-drawer dresser is available in a white stain finish and measures 63x37 3/4 inches. It i... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| colly+md | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What's the price of the RAST 3-drawer dresser?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The price of the RAST 3-drawer dresser is $59.99.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The price of the RAST 3-drawer dresser is $59.99.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The price of the RAST 3-drawer dresser is $59.99.... |
| markcrawl | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q5: What bed frames does IKEA sell?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including platform beds, storage beds, daybeds, loft beds, bunk b... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including platform beds, storage beds, daybeds, loft beds, bunk b... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including twin beds, single beds, upholstered beds, daybeds, bed ... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including twin beds, single beds, bed frames, upholstered beds, d... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | IKEA sells a variety of bed frames including platform beds, storage beds, daybeds, loft beds, bunk b... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| markcrawl | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: Show me IKEA's sofa and armchair selection**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of sofas and armchairs, including:  1. **Sofas & Sectionals**: Options include... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of sofas and armchairs, including:  - **Sofas & Sectionals**: Options like lov... |
| markcrawl | 5 | 5 | 4 | 5 | 4.8 | You can explore IKEA's sofa and armchair selection by visiting their website or store, where you wil... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q7: What dressers and storage drawers does IKEA offer?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including:  - STORKLINTA series (available in... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including:  1. **GULLABERG dressers** - Elega... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | IKEA offers a variety of dressers and storage drawers, including:  1. GULLABERG series - elegant sto... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | IKEA offers the following dressers and storage drawers:  1. STOREMOLLA 8-drawer dresser (available i... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | IKEA offers the GULLABERG dressers, which feature an elegant storage furniture series in traditional... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | IKEA offers the following dressers and storage drawers:  1. GULLABERG dressers - an elegant storage ... |
| playwright | 4 | 5 | 3 | 4 | 4.0 | IKEA offers the GULLABERG dressers, which are an elegant storage furniture series in traditional des... |

**Q8: How much is the STOREMOLLA 8-drawer dresser at IKEA?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 1 | 5 | 1 | 1 | 2.0 | The STOREMOLLA 8-drawer dresser is priced at $599.99.... |
| crawl4ai-raw | 1 | 5 | 1 | 1 | 2.0 | The STOREMOLLA 8-drawer dresser is priced at $599.99.... |
| scrapy+md | 1 | 5 | 1 | 1 | 2.0 | The STOREMOLLA 8-drawer dresser is priced at $599.99.... |

</details>

## newegg

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawl4ai | 4.12 | 4.62 | 4.25 | 4.38 | 4.34 ±0.75 |
| crawl4ai-raw | 4.12 | 4.62 | 4.25 | 4.38 | 4.34 ±0.75 |
| colly+md | 4.00 | 4.50 | 4.00 | 4.25 | 4.19 ±0.63 |
| playwright | 3.50 | 3.25 | 2.62 | 2.88 | 3.06 ±0.72 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for newegg</summary>

**Q1: What graphics cards are available at Newegg?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 3 | 5 | 4 | 4 | 4.0 | Newegg offers a wide selection of graphics cards, including high-performance models like the GeForce... |
| crawl4ai-raw | 3 | 5 | 4 | 4 | 4.0 | Newegg offers a wide selection of graphics cards, including high-performance models like the GeForce... |
| colly+md | 2 | 5 | 4 | 4 | 3.8 | The available graphics cards at Newegg include:  1. GIGABYTE Gaming GeForce RTX 5090 Graphics Card 2... |
| playwright | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What laptops does Newegg sell?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Newegg sells a variety of laptops from brands such as Lenovo, HP, DELL, Acer America, ASUS, MSI, GIG... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Newegg sells a variety of laptops from brands such as Lenovo, HP, DELL, Acer America, ASUS, MSI, GIG... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Newegg sells a variety of laptops including business laptops, ultraslim laptops, 2-in-1 laptops, gam... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |

**Q3: How much does the AMD Ryzen 7 9800X3D CPU cost?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The AMD Ryzen 7 9800X3D CPU costs $464.00.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The AMD Ryzen 7 9800X3D CPU costs $506.99.... |
| playwright | 4 | 5 | 4 | 4 | 4.2 | The AMD Ryzen 7 9800X3D CPU costs $320.00.... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q4: What is the price of the Intel Core i9-14900K?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The price of the Intel Core i9-14900K is $599.00.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The price of the Intel Core i9-14900K is $599.00.... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q5: Tell me about the GIGABYTE GeForce RTX 5090 graphics card**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| colly+md | 2 | 5 | 4 | 4 | 3.8 | The GIGABYTE GeForce RTX 5090 is a flagship graphics card powered by the Blackwell architecture. It ... |
| playwright | 3 | 3 | 2 | 2 | 2.5 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q6: How much does the SAPPHIRE Radeon RX 9070 XT cost?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | The SAPPHIRE Radeon RX 9070 XT costs $769.99, with a regular price of $879.99.... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | The SAPPHIRE Radeon RX 9070 XT costs $769.99, with a regular price of $879.99.... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The SAPPHIRE Radeon RX 9070 XT costs $769.99.... |
| playwright | 3 | 3 | 3 | 3 | 3.0 | I cannot answer this based on the provided context.... |

**Q7: What ASUS TUF gaming laptops are available on Newegg?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| colly+md | 5 | 5 | 5 | 5 | 5.0 | The available ASUS TUF gaming laptops on Newegg include:  1. **ASUS TUF Gaming A16** - 16" FHD+ 165 ... |
| crawl4ai | 2 | 5 | 4 | 4 | 3.8 | The available ASUS TUF gaming laptops on Newegg are:  1. **ASUS TUF Gaming - 18" WQXGA 240 Hz**    -... |
| crawl4ai-raw | 2 | 5 | 4 | 4 | 3.8 | The available ASUS TUF gaming laptops on Newegg are:  1. **ASUS TUF Gaming - 18" WQXGA 240 Hz**    -... |
| playwright | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |

**Q8: What electronics categories does Newegg offer?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | Newegg offers electronics categories including laptops, gaming consoles, home electronics, PC compon... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | Newegg offers electronics categories including laptops, gaming consoles, home electronics, PC compon... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | Newegg offers electronics categories including gaming laptops, home tech essentials, home audio, kit... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | Newegg offers a variety of electronics categories including:  - Components & Storage (CPUs, memory, ... |

</details>

## propublica

| Tool | Correctness | Relevance | Completeness | Usefulness | Overall |
|---|---|---|---|---|---|
| crawlee | 4.83 | 4.67 | 4.33 | 4.67 | 4.62 ±0.64 |
| playwright | 4.67 | 4.67 | 4.33 | 4.33 | 4.50 ±0.73 |
| markcrawl | 4.33 | 4.50 | 4.17 | 4.33 | 4.33 ±0.83 |
| colly+md | 4.33 | 4.50 | 4.17 | 4.33 | 4.33 ±0.83 |
| crawl4ai-raw | 4.50 | 4.17 | 3.83 | 4.17 | 4.17 ±0.98 |
| scrapy+md | 4.50 | 4.17 | 3.67 | 4.17 | 4.12 ±0.95 |
| crawl4ai | 4.17 | 4.00 | 3.50 | 4.00 | 3.92 ±1.03 |

> Scores are 1-5 averages. See summary table legend for dimension definitions.

<details>
<summary>Query-by-query scores for propublica</summary>

**Q1: What ProPublica investigations cover criminal justice?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| crawlee | 5 | 5 | 5 | 5 | 5.0 | ProPublica investigations covering criminal justice include:  1. **Prosecutors Had a Drugs-for-Votes... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | ProPublica investigations covering criminal justice include:  1. **Prosecutors Had a Drugs-for-Votes... |
| crawl4ai-raw | 5 | 5 | 4 | 5 | 4.8 | ProPublica investigations covering criminal justice include:  1. "Prosecutors Had a Drugs-for-Votes ... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | ProPublica investigations covering criminal justice include reporting on why youths at a juvenile co... |
| crawl4ai | 3 | 4 | 3 | 4 | 3.5 | ProPublica investigations covering criminal justice include:  1. "Prosecutors Had a Drugs-for-Votes ... |
| markcrawl | 2 | 4 | 3 | 3 | 3.0 | ProPublica investigations covering criminal justice include:  1. **The Militia and the Mole** - A wi... |
| colly+md | 2 | 4 | 3 | 3 | 3.0 | ProPublica investigations covering criminal justice include:  1. Prosecutors had a drugs-for-votes s... |

> **Corr** = correctness, **Rel** = relevance, **Comp** = completeness, **Use** = usefulness, **Avg** = average of the four dimensions (1-5).

**Q2: What is ProPublica reporting about healthcare?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | ProPublica is reporting on various issues in healthcare, including the impact of private equity on h... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | ProPublica reports on various healthcare issues, including the quality of care in emergency rooms, t... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | ProPublica reports on various healthcare issues, including the quality of care in emergency rooms, t... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | ProPublica is reporting on various issues related to healthcare, particularly focusing on health ins... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | ProPublica is reporting on various healthcare issues, including the subpar care provided by Armor He... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | ProPublica is reporting on various healthcare issues, including the lawsuit seeking medical stockpil... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | ProPublica is reporting on various healthcare issues, including subpar care in jails, the impact of ... |

**Q3: What ProPublica articles discuss politics and government accountability?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | ProPublica articles that discuss politics and government accountability include:  1. **The White Hou... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | ProPublica articles discussing politics and government accountability include:  1. "Prosecutors Had ... |
| crawlee | 5 | 5 | 4 | 5 | 4.8 | The ProPublica articles that discuss politics and government accountability include:  1. "Prosecutor... |
| playwright | 4 | 5 | 4 | 4 | 4.2 | The ProPublica articles that discuss politics and government accountability include:  1. "Prosecutor... |
| crawl4ai-raw | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| scrapy+md | 3 | 2 | 2 | 2 | 2.2 | I cannot answer this based on the provided context.... |
| crawl4ai | 3 | 2 | 1 | 2 | 2.0 | I cannot answer this based on the provided context.... |

**Q4: What environmental or climate investigations does ProPublica have?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | ProPublica conducted an investigation into livestock grazing on public lands, revealing the subsidie... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | ProPublica has conducted several environmental and climate investigations, including:  1. Reporting ... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | ProPublica has conducted several environmental and climate investigations, including:  1. Reporting ... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | ProPublica has conducted several environmental and climate investigations, including:  1. Investigat... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | ProPublica has conducted several environmental and climate investigations, including:  1. A series o... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | ProPublica has conducted several environmental and climate investigations, including:  1. Reporting ... |
| scrapy+md | 5 | 5 | 4 | 5 | 4.8 | ProPublica covers various environmental issues, including health impacts related to air quality, pol... |

**Q5: What ProPublica stories cover immigration?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 5 | 5 | 5 | 5 | 5.0 | The ProPublica stories covering immigration include:  1. **The White House Intervened on Behalf of A... |
| crawl4ai | 5 | 5 | 5 | 5 | 5.0 | ProPublica stories covering immigration include:  1. "I Lost Everything”: Venezuelans Were Rounded U... |
| crawl4ai-raw | 5 | 5 | 5 | 5 | 5.0 | ProPublica stories covering immigration include:  1. "I Lost Everything”: Venezuelans Were Rounded U... |
| scrapy+md | 5 | 5 | 5 | 5 | 5.0 | The ProPublica stories that cover immigration include:  1. An investigation into how many U.S. citiz... |
| crawlee | 5 | 5 | 5 | 5 | 5.0 | ProPublica stories that cover immigration include:  1. "Fear and Opportunity: Immigration Scams Surg... |
| colly+md | 5 | 5 | 5 | 5 | 5.0 | ProPublica stories that cover immigration include:  1. "Fear and Opportunity: Immigration Scams Surg... |
| playwright | 5 | 5 | 5 | 5 | 5.0 | ProPublica stories that cover immigration include:  1. "Fear and Opportunity: Immigration Scams Surg... |

**Q6: What is the main ProPublica homepage with featured stories?**

| Tool | Corr | Rel | Comp | Use | Avg | Answer (truncated) |
|---|---|---|---|---|---|---|
| markcrawl | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawl4ai-raw | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| scrapy+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| crawlee | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| colly+md | 4 | 3 | 2 | 3 | 3.0 | I cannot answer this based on the provided context.... |
| playwright | 4 | 3 | 2 | 2 | 2.8 | I cannot answer this based on the provided context.... |

</details>

## Methodology

- **Answer generation:** `gpt-4o-mini` with temperature=0, max_tokens=500
- **Answer judging:** `gpt-4o-mini` scores correctness, relevance, completeness, usefulness (1-5)
- **Retrieval:** Top-10 chunks by cosine similarity (same as retrieval benchmark)
- **Chunking:** Markdown-aware, 400 word max, 50 word overlap
- **Embedding:** `text-embedding-3-small`
- **Same pipeline for all tools** — only crawler output quality varies

## See also

- [RETRIEVAL_COMPARISON.md](RETRIEVAL_COMPARISON.md) — retrieval doesn't differ much, but answers do
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what the quality gap costs at scale
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions

