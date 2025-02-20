import openai

class BrochureCreation:
    def __init__(self, model, api_key):
        self.model = model
        openai.api_key = api_key

    def create_brochure(self, company_name, relevant_links):
        """
        Generates the brochure based on the relevant links selected.
        """
        truncated_links = self.truncate_links(relevant_links)

        messages = self.create_brochure_prompt(company_name, truncated_links)

        response = openai.chat.completions.create(
            model=self.model, 
            messages=messages,
            max_tokens=1200  
        )

        brochure_content = response.choices[0].message.content.strip() 
        return brochure_content

    def create_brochure_prompt(self, company_name, relevant_links):
        """
        Creates a prompt to instruct OpenAI to generate a natural-sounding company brochure 
        based on selected links.
        """
        prompt = (
            f"Imagine you are a skilled marketing writer tasked with creating a compelling company brochure for {company_name}. "
            "The brochure should read naturally and persuasively, capturing the essence and personality of the company, always staying professional and political."
            "It will be used by job seekers, marketing strategist, and businesses to understand the company, use the most important elements of a brochure."
            "It should tell a story that flows smoothly from one section to the next while highlighting the key aspects of the business,.\n\n"
        )
        
        prompt += "Below are some categorized key links that provide essential information about the company. Use these details as inspiration to craft the brochure:\n"
        
        for category, links in relevant_links.items():
            prompt += f"\n- **{category}**: "
            prompt += ", ".join(links)
        
        prompt += (
            "\n\nNow, write the brochure in a friendly yet professional tone. "
            "Avoid a rigid, structured format; instead, use a narrative style that includes an introduction, a body that discusses the company's "
            "history, products, services, values, and culture, and a closing section with contact information. "
            "The text should be engaging, informative, and easy to read, as if written by a professional copywriter for a top-tier company brochure."
        )
        
        return [{"role": "user", "content": prompt}]

    
    def truncate_links(self, relevant_links):
        """
        Truncate the links to ensure the message stays within the token limit.
        This function reduces the size of the input prompt.
        """
        truncated_links = {}
        for category, links in relevant_links.items():
            truncated_links[category] = links[:6]  
        return truncated_links