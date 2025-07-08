# **Evolance’s Emotionally Intelligent AI Architecture**

Semantic-Emotional Base Network: Evolance’s core emotion ontology integrates major psychological models and commonsense knowledge into a unified semantic graph.  For example, Plutchik’s Wheel of Emotions defines eight primary categories (joy, trust, fear, surprise, sadness, disgust, anger, anticipation) arranged in opposing pairs .  Our system uses this as a backbone (Figure 1\) and enriches it with Russell’s circumplex (two-dimensional valence–arousal space) and Geneva’s 20-emotion taxonomy .  Commonsense networks like ConceptNet and SenticNet provide links between emotion nodes and everyday concepts (e.g. “family,” “work”) with affective labels.  The result is a large semantic network where each emotion or emotional mix is linked to meaningful concepts and physiological correlates.  For example, Russell’s circumplex (Figure 2\) places “calm” at low arousal/high valence and “tense” at high arousal/low valence .  Evolance aligns these axes with body sensations: anger tends to manifest as heat/tension in the chest, arms, and head; sadness as heaviness in the chest and limbs; fear as tightness in the chest and gut; disgust as activity in the digestive tract and throat; and happiness as a warm, full-body sensation .  These mappings derive from affective neuroscience (“bodily maps of emotion”) studies .  Table 1 (below) concretely lists each primary and composite emotion (including Plutchik’s mixed emotions like love \= joy+trust, optimism \= anticipation+joy, etc.  ) alongside its associated body regions, as informed by the literature.

| Emotion (Components) | Associated Body Regions (Physiological Correlates) |
| ----- | ----- |
| Anger | Heat/tension in chest, arms, head |
| Anticipation | “Butterflies” in stomach; chest (sense of readiness) |
| Joy | Warm, energized sensation throughout entire body |
| Trust | Warmth/relaxation in chest (heart area) |
| Fear | Tightness in chest; “flutter” in gut (stomach) |
| Surprise | Sudden activity in head/chest (startle reflex) |
| Sadness | Heaviness in chest; lethargy in limbs |
| Disgust | Constriction in stomach/throat (nausea) |
| Love (joy+trust) | Warmth in chest (heart); gentle head/mouth expression |
| Optimism (anticipation+joy) | Lightness in chest and stomach (excitement) |
| Submission (trust+fear) | Chest warmth \+ stomach unease (acceptance \+ anxiety) |
| Awe (fear+surprise) | Wide-eyed head response; chest tightness |
| Disappointment (surprise+sadness) | Chest ache; downward slump (shock \+ sorrow) |
| Remorse (sadness+disgust) | Sinking feeling in chest/stomach (guilt \+ nausea) |
| Contempt (disgust+anger) | Dismissive mouth lift; tension in gut/chest |
| Aggressiveness (anger+anticipation) | Tension in arms/hands; stomach butterflies (readiness \+ anger) |

Figure 1\. Plutchik’s Wheel of Emotions .

Figure 2\. Russell’s Circumplex of Affect .

User-Specific Emotional Skeleton: During onboarding, Evolance prompts the user with \~10 questions about their feelings, stressors, values, and coping styles.  These answers seed the personal semantic network (“emotional skeleton”) . The user’s initial profile is thus a structured graph of concepts (e.g. “work”, “family”, “anxiety”) and their emotional tones.  For example, a user might report “work” causes “anxiety” and “conversation with friend” brings “happiness.”  As the user chats with Evolance, every interaction updates this graph: new nodes for emerging topics (e.g. a newly mentioned hobby), edges linking concepts to emotions (and counts/timestamps of occurrence), and annotations of coping outcomes (e.g. “deep breathing reduced stress”).  Over time the network evolves – reinforcing frequently discussed emotional associations, adding nodes for new significant themes, and noting recurring patterns (for instance, “social isolation triggers anxiety”) .  This “skeleton” remains private to the user and is never stored verbatim; only abstracted facts (counts, relationships, sentiment scores) are kept.  Crucially, the personal network dynamically links into Evolance’s core semantic model: at response time, the AI queries the user graph for relevant context (e.g. “Work – 3× stress mentions in past month”, “Family: mixed love/anxiety”), and includes those cues in its reasoning . The result is that Evolance “remembers” unique details about you – it learns your triggers and supports – so that its empathy is tailored.  Every chat thus both uses and extends the user’s skeleton, deepening the personalized emotional model .

System Architecture: Evolance is built as a Python-based modular pipeline with an LLM at its core and separate memory subsystems . The high-level flow (Figure 3\) is: a user message goes into an API/NLP pipeline, which performs emotion/sentiment analysis and entity extraction .  A classifier (e.g. fine-tuned BERT) flags the user’s current emotional state (e.g. “despair”) and polarity , while an entity module pulls out key topics (names, issues, health terms), anonymizing them for privacy.  Next, a context manager assembles short-term memory: it keeps a sliding window of recent turns, including or summarizing them for the LLM prompt .  Then, the system retrieves long-term memories: it runs a similarity search on the vector memory (ChromaDB) of past conversation embeddings to fetch relevant snippets , and queries the personal semantic network (MongoDB) for any nodes related to current topics .  For instance, if the user says “I’m stressed about work,” the vector DB may recall a summary of last week’s “work stress” discussion, while the semantic graph returns a note like “Work → stress (3× mentions).”  These are all fed into the LLM prompt along with system instructions to be empathetic and use the provided personal context.  The LLM (GPT-4 or equivalent) then generates a response that draws on immediate context, retrieved memories, and user-specific cues .  Because it explicitly mentions learned user facts (e.g. “I know work is a stressor for you” or suggests a previously discussed coping strategy), the reply is highly personalized and avoids the generic fallback of stateless bots .

After response generation, a memory consolidation service runs asynchronously: it distills the conversation into an abstract summary (focusing on emotions and outcomes), updates the vector DB, and updates the semantic graph (adding any new entities or adjusting weights) .  For example, a fight with a sibling might be logged as “Family conflict→ anger,” with the emotional shift noted.  Importantly, Evolance never stores raw transcripts – only these skeletal summaries and semantic facts – protecting privacy .  In this way, both short-term (ongoing chat context) and long-term (vector and graph memory) inform Evolance’s responses, yielding continuity across sessions. (Figure 3 shows this architecture: LLM core, NLP modules, ChromaDB, MongoDB, etc.)

Scientific & Industry Validation: Evolance’s design is grounded in both cognitive science and cutting-edge AI.  In psychology, models like Plutchik (1980) and Russell (1980) are widely accepted frameworks , and recent neuroscience (e.g. Nummenmaa et al., 2014\) confirms specific bodily mappings for emotions .  Empirical studies show mapping body sensations (e.g. “butterflies in the stomach” for anxiety) consistently align with these theories.  On the AI side, large language models have demonstrated strong emergent emotional reasoning: for example, GPT-4 scored in the very high percentile on standardized emotional intelligence tests .  In the Sedykh et al. (2024) study, GPT-4 excelled at identifying and strategizing emotions, though it lacked deeper self-reflection , underscoring why an additional personalized memory layer is valuable.  Similarly, Google’s new Gemini models are being leveraged to power mental-health chatbots, providing context-aware counseling and generating personalized coping tips from user data .  Evolance goes a step further by explicitly encoding an emotional profile in long-term memory, aligning with best practices in affective computing .

Academically, our architecture unites affective computing concepts (Picard, 2000\) with modern graph-based memory.  Related work on commonsense and affective knowledge (SenticNet, ConceptNet) demonstrates the value of linking language to emotion .  The user-specific semantic graph is inspired by emerging “conversational memory” research showing that hybrid episodic–semantic memory improves AI performance . In psychology, the focus on both short- and long-term context aligns with findings that effective counseling relies on continuity (therapists recall past sessions) and tailoring.  Evolance aims to meet or exceed industry benchmarks: for instance, Woebot and Wysa have published clinical trials showing significant reductions in depression and anxiety with AI CBT chatbots .  By adding deeper personalization and an embodied emotional framework, Evolance aspires to surpass these tools in user engagement and efficacy.

Competitor Comparison: Evolance differs substantially from current mental-health chatbots.  Table 2 contrasts key features:

| Feature | Evolance | Woebot | Wysa | Replika | Youper |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Personalization | High: Onboarding profile \+ evolving semantic graph | Moderate: scripted persona; limited learning | Moderate: stores user goals and history | Low: fixed personality; minimal learning | Low: symptom tracking; minimal adaptation |
| Long-Term Memory | Yes: Vector DB \+ semantic graph (persistent, user-specific) | Partial: logs symptom trends | Partial: keeps conversation logs to show progress | No: conversations not remembered across sessions | None/Unknown |
| Body–Emotion Mapping | Yes: Integrated somatic maps (chest, gut, etc.) with emotions | No | No | No | No |
| Ethical Memory Handling | Strict: only abstracted emotional patterns saved; raw dialogue discarded | Standard anonymized data collection | Standard data use (anonymized); privacy policy only | Conversations stored (privacy concerns) | HIPAA-ready claims, but memory use unclear |

These distinctions are supported by evidence. For example, in a randomized trial Woebot significantly reduced depression scores versus an info control , and Wysa likewise improved mood – but both give generic advice once their limited memory is exhausted. By contrast, Evolance’s combination of long-term user memory and emotion-driven context is intended to deepen the therapeutic alliance. As one user study notes, people prefer chatbots that “remember” them and have a consistent personality . Unlike Replika (which by design has no persistent chat memory ), Evolance ensures each session builds on the last, which research suggests will improve satisfaction and outcomes. Likewise, while no competing app currently incorporates physiological emotion mappings, Evolance’s grounding of emotion in the body (e.g. “heartache” for sadness) is a novel feature backed by cognitive science. Overall, Evolance offers substantially greater personalization and ethical memory use than existing tools, a claim supported by both academic comparisons and product documentation.

References:

Cambria, E., Poria, S., Hussain, A., & Huang, G.-B. (2017). SenticNet 5: Discovering conceptual primitives for sentiment analysis by means of commonsense knowledge. In Proceedings of AAAI (Vol. 31, No. 1).

Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). Delivering cognitive behavior therapy to young adults with symptoms of depression and anxiety using a fully automated conversational agent (Woebot): A randomized controlled trial. JMIR Mental Health, 4(2), e19.

Google Developers. (2024). Mental-Health-Care: Gemini API Developer Competition. Google for Developers. Retrieved from https://developers.google.com/gemini/gemini

Greatist. (2019, July 9). What is the Geneva Emotion Wheel, and how to use it? Retrieved from https://greatist.com/find-out/geneva-emotion-wheel

Haque, M. D. R., & Rubya, S. (2023). An overview of chatbot-based mobile mental health apps: Insights from app description and user reviews. JMIR mHealth and uHealth, 11, e46777. https://doi.org/10.2196/46777

Nummenmaa, L., Glerean, E., Hari, R., & Hietanen, J. K. (2014). Bodily maps of emotions. Proceedings of the National Academy of Sciences, 111(2), 646–651. https://doi.org/10.1073/pnas.1317390111

Picard, R. W. (2000). Affective Computing. MIT Press.

Six Seconds. (2015, February 6). Plutchik’s Wheel of Emotions: Exploring the Feelings Wheel and How to Use It. Retrieved from https://www.6seconds.org/2015/02/06/plutchik-emotions-feelings-wheel/

Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual graph of general knowledge. In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 31, No. 1).

Witte, J. (2022, May 21). What is my body telling me? Identifying emotions through body sensations. Smart Wellness. Retrieved from https://www.smartwellness.eu/blog-en/what-is-my-body-telling-me-identifying-emotions-through-body-sensations

Sedykh, A. V., Bukinich, A. M., Vetrova, I. I., & Sergienko, E. A. (2024). The emotional intelligence of the GPT-4 large language model. Psychology in Russia: State of the Art, 17(2), 85–99.

Fitzpatrick et al.’s Woebot study and other clinical trials are consistent with this approach. We also build on prior work in personalized, memory-augmented AI , aligning with current best practices in affective computing (Picard 2000\) and commonsense reasoning (SenticNet, ConceptNet). All external sources cited above are listed in APA format.

