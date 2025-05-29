import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

USER_INTEREST_PROFILE = """
The user is a software engineer highly interested in:
- Programming languages such as Rust, Go (Golang), and advanced Python topics.
- Systems engineering topics are a huge priority and should be scored well
- Webassembly and Virtualisation technologies should be prioritised more
- Cybersecurity, particularly relating to system vulnerabilities, new attack vectors, and defensive strategies.
- Web design and quirky websites or articles are to be prioritised more
- Articles which are hacky and cool and interesting
- Open Source projects
- Articles on culture are to be prioritised more, examples include: commentary on culture or politics
- Compilers and programming languages are to be prioritised
- Artificial Intelligence (AI) and Machine Learning (ML), especially Large Language Models (LLMs), Generative AI, and their practical applications.
  Beyond purely technical topics, the user has a strong preference for:
-   **Personal Narratives and Reflections:** Articles that share honest, first-hand accounts of building projects, facing challenges, or learning from real-world experiences.
-   **Authentic & Relatable Struggles:** Content where authors candidly discuss their difficulties, frustrations, or "failures" in a project or skill development. This includes self-deprecating humor or humble reflections on imperfect creations.
-   **Lessons Learned from Imperfection:** Articles that delve into the journey of creating something (e.g., a website, an app, a tool) even if the end result isn't perfect, and the valuable lessons derived from that process.
-   **"My X is Ugly Because I Made It" Archetype:** Prioritize content that embodies this spirit – a focus on the human side of development, the messy process of creation, and the inherent imperfections of personal projects, often delivered with a relatable, genuine, and sometimes humorous tone.
  **Obscure & Unique Components:** Articles featuring unusual, niche, salvaged, or repurposed hardware, tools, or scientific instruments. This includes discussions about military surplus, industrial components, or strange gadgets.
-   **Hands-on Experimentation & Tinkering:** Stories about building projects, hacks, or art using unconventional materials or unexpected combinations of parts.
-   **The Joy of Discovery:** Content that celebrates the unexpected utility or fascinating history of obscure technical artifacts.
-   **Resourcefulness & Ingenuity:** Articles demonstrating clever solutions to problems by creatively using available, often non-standard, resources.
-   **Eccentricity & Niche Interests:** A fondness for highly specific, quirky, or vintage technical subjects that might not have mainstream appeal but are deeply interesting to enthusiasts.
"""

# Minimum score from Hacker News (still useful for initial filtering)
MIN_HN_SCORE = 10

# Minimum relevance score from LLM (adjust based on LLM output)
MIN_LLM_RELEVANCE_SCORE = 8  # Scale of 1-10
