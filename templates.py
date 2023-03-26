WRITEMORE_DESCRIPTION = """
Your task is to write content on a topic descibed by the Writemore project.
"""

CONTENT_ROADMAP_TEMPLATE = template = """{writemore_description}

Create a content roadmap. The roadmap is a list of 10 elements,
all coherently organized to fullfill the Writemore project.
Each element is a paragraph of 3-6 sentences.
The content roadmap must be formatted in a numberest list,
with each element separated by 2 newlines.

You must be clear and concise.

Writemore project: {writemore_project}
Content roadmap:
"""

CONTENT_TEMPLATE = """{writemore_description}

Writemore project: {writemore_project}

Content roadmap:
{content_roadmap}

You have to create new content based on the content roadmap.
ONLY create content for the content element specified below.
Content length should be in ball park of 500 words.

Content element: write chatper {content_element}
Content:"""
