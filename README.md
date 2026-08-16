Based on the **DeepAgents + LangGraph** unified workflow engine, with a focus on the Douyin e-commerce risk control vertical, build a series of intelligent agents for Douyin e-commerce governance.

### Workflow Architecture

The runtime pipeline view: a request flows through the FastAPI/SSE entry, is assembled by DeepAgents, and executes on a LangGraph `CompiledStateGraph`. State passes through middleware pre-processing, the LLM node, and tool routing; tool results are written back to State to form the agentic loop.

![Main Workflow](./mainchain.svg)

### Module Architecture

The component view: the system is composed of Planning, ToolCall (Tool Index → Retriever → Tool Call → Tool Executor → Environment), and Memory Folding modules, backed by Tool/Skill/Agent registries and RPC/Web/Lark deployments.

![Module Architecture](./mode.svg)

### Subagent Workflow

At the agent level, a subagent is a lightweight agent with path-planning capability. Its execution graph is composed of three kinds of nodes — LLM nodes, code nodes, and tool nodes — that the planner routes between to carry out a single inspection task.

![Subagent Workflow](./Frontend%20Inspection/Link%201/inspect_agent/inspect_beef_and_egg_live/subagent_workflow.svg)