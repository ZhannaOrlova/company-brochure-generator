import openai

class LinkSelection:
    def __init__(self, model, api_key):
        self.model = model
        openai.api_key = api_key

    def select_relevant_links(self, website):
        """
        Selects the most relevant links for the company's brochure.
        """
        # Create the messages to send to GPT based on the website
        messages = self.create_prompt(website)
        
        # Make the request to OpenAI using the chat API for conversation-based models
        response = openai.chat.completions.create(
            model=self.model,  # e.g., 'gpt-4'
            messages=messages,
            max_tokens=100
        )

        # Extract relevant links from the response
        result = response.choices[0].message.content  # Access content properly
        print(f"Relevant links response: {result}")
        
        # Sanitize the result to remove any potential issues and parse it
        try:
            relevant_links = self.parse_links(result)
        except Exception as e:
            print(f"Error parsing response: {e}")
            relevant_links = {}

        print(f"Relevant links parsed: {relevant_links}")
        
        # Ensure the 'links' key exists
        return relevant_links

    def parse_links(self, result):
        """
        Parse the result from OpenAI and convert it into a dictionary of relevant links.
        """
        # Initialize an empty dictionary for the links
        links_dict = {}

        # Example: Look for patterns in the text and extract them
        lines = result.split('\n')
        category = None
        links = []

        for line in lines:
            # Detect new categories based on markdown-style headings
            if line.startswith('###'):
                if category:
                    links_dict[category] = links  # Store links for the previous category
                category = line.strip('#').strip()  # Capture the new category
                links = []  # Reset links list for the new category
            elif line.startswith('-'):
                # Extract the link from the markdown format
                link = line.split('(')[1].split(')')[0]
                links.append(link)
        
        # Don't forget to store the last category's links
        if category:
            links_dict[category] = links

        return links_dict

    def create_prompt(self, website):
        """
        Creates the prompt for OpenAI using the website's links.
        This will need to be structured according to the model's needs.
        """
        # Example prompt structure:
        user_prompt = f"Here is the list of links on the website of {website.url}:\n"
        user_prompt += "\n".join(website.links)
        user_prompt += "\nPlease decide which of these links are most relevant for a company brochure, such as links to an About page, Careers page, or Products/Services pages, do not exceed the top 5 links."

        # Return as a list of messages (this structure works for chat-based models)
        return [{"role": "user", "content": user_prompt}]
