from bs4 import BeautifulSoup
import requests

class Scrapper:
    def __init__(self, subject):
        self.subject = subject
        self.base_url = 'https://en.wikipedia.org/wiki/'
        self.url = self.get_wikipedia_url()

    def get_wikipedia_url(self):
        subject_formatted = self.subject.replace(' ', '_')
        return self.base_url + subject_formatted

    def fetch_page(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content  # Use content instead of text to ensure correct parsing
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def get_headings(self, soup):
        headings = soup.find_all(['h2', 'h3', 'h4'])
        heading_list = []

        for heading in headings:
            heading_text = heading.get_text().strip()
            heading_list.append(heading_text)

        return heading_list

    def get_section_content(self, soup, selected_heading):
        # Find the selected heading
        for heading in soup.find_all(['h2', 'h3', 'h4']):
            heading_text = heading.get_text().strip()

            if heading_text == selected_heading:
                section_content = []
                # Collect all siblings until the next heading is found
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h2', 'h3', 'h4']:
                        break
                    section_content.append(str(sibling))  # Store the HTML as string
                return '\n'.join(section_content) if section_content else "No content found in the selected section."

        print(f"Section '{selected_heading}' could not be found.")
        return None

    def run(self):
        page_content = self.fetch_page()

        if not page_content:
            return

        soup = BeautifulSoup(page_content, 'html.parser')

        # Get and display all the headings
        headings = self.get_headings(soup)
        if not headings:
            print("No headings found on the page.")
            return

        print("\nAvailable sections:")
        for i, heading in enumerate(headings):
            print(f"{i + 1}. {heading}")

        # Prompt the user to choose a section
        try:
            choice = int(input("\nEnter the number of the section you want to view: "))
            if choice < 1 or choice > len(headings):
                print("Invalid choice.")
                return
            selected_heading = headings[choice - 1]

            # Get and display the selected section content
            content = self.get_section_content(soup, selected_heading)
            if content:
                print(f"\nContent under '{selected_heading}':\n")
                # Print the raw HTML for better inspection
                print(content)
            else:
                print(f"Content for section '{selected_heading}' could not be retrieved.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    subject = input("Enter the subject you want to search on Wikipedia: ")
    scrapper = Scrapper(subject)
    scrapper.run()
#this is bugged as hell