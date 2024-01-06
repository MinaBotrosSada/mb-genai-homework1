import feedparser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from vertexai.language_models import TextGenerationModel
import vertexai


# Fetch the RSS feeds for the first X articles
def fetchRSS(URL, limit=50):
    RSS = feedparser.parse(URL)
    return RSS.entries[:limit]


# Fetch the HTML content of the article
def fetchBeautifulHTMLContent(URL):
    url = URL
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    html_text = '\n'.join(chunk for chunk in chunks if chunk)

    return html_text    


import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

      
def run():
    import vertexai
    from vertexai.preview.language_models import TextGenerationModel

    st.write("# Welcome to MB's Streamlit GenAI RSS Summarizer! 👋")

    title = st.text_input('RSS Feed URL', 'https://moxie.foxnews.com/google-publisher/latest.xml')
    st.write('The current RSS Feed URL is', title)
    
    if st.button('Summarize', type="primary"):        
        if title is None:
            title='https://moxie.foxnews.com/google-publisher/latest.xml'

        st.write('Summarization in progress...')

        vertexai.init(project="minab-ddf-sandbox", location="us-central1")
        parameters = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_k": 40, 
            "top_p": 0.8
        }
        model = TextGenerationModel.from_pretrained("text-bison")

         # Load the model            
        list_of_articles = fetchRSS(title, 10)

        # Iterate over the list of articles
        for article in list_of_articles:
            st.markdown(f"### {article.title}")
                        
            prompt = fetchBeautifulHTMLContent(article.link)
                        
            response = model.predict(
            f"""Summarize this article in no more than 4 sentences, with a new line after each sentence without bullet points

            input: Adobe shares dropped more than 6% in extended trading Wednesday after the software maker posted a lighter-than-expected forecast for 2024.
            Here’s how the company did, compared to consensus estimates from LSEG, formerly known as Refinitiv:
            Earnings per share: $4.27, adjusted vs. $4.14 expected
            Revenue: $5.05 billion vs. $5.03 billion expected

            Revenue grew almost 12% from a year ago in the fiscal fourth quarter, which ended Dec. 1, according to a statement. Net income increased 26% to $1.48 billion, or $3.23 per share, up from $1.18 billion, or $2.53 per share, in the year-ago quarter.
            While results for the latest quarters topped estimates, Adobe’s guidance for the new fiscal year disappointed Wall Street.
            Adobe called for fiscal 2024 earnings per share of $17.60 to $18 on $ $21.3 billion to $21.5 billion in revenue. Analysts polled by LSEG had expected $18 in adjusted earnings per share and $21.73 billion in revenue.
            Executives continue to look carefully at spending, Anil Chakravarthy, president of Adobe’s experience business that includes marketing software, said on a conference call with analysts.
            Adobe’s CEO, Shantanu Narayen, acknowledged questions about forward-looking recurring revenue the company could derive from subscriptions to the Creative Cloud software bundle. During the quarter Adobe increased the costs of some subscriptions.

            ’We’re extremely confident about how that continues to be a growth business, and perhaps the pricing impact was overestimated,” Narayen said.
            Also in the quarter, Adobe’s Firefly generative artificial intelligence features became available in the Photoshop and Illustrator programs for Creative Cloud subscribers. An enterprise version of the Firefly web app that can create images based on a few words of human input also became available.
            Adobe remains focused on closing the $20 billion Figma acquisition it announced in September 2022. The company said it disagrees with findings from regulators in the European Commission and the U.K. and that it’s responding to regulators. The U.S. Department of Justice has also been looking into the planned deal.
            “While the DOJ does not have a formal timeline to decide whether to bring a complaint, we expect a decision soon,” Narayen said.
            The guidance does not factor in impact from Figma.
            Adobe said in a separate regulatory filing that it has been working with the U.S. Federal Trade Commission on an inquiry over cancellation and subscription practices in connection with the Restore Online Shoppers’ Confidence Act. The FTC told the company in November that it had the authority to enter into consent negotiations to see if a settlement could be reached, according to the filing. Adobe sees its past behavior as lawful and said the matter might have a material effect on financial performance.
            Prior to the after-hours move, Adobe shares were up almost 86% this year, outperforming the S&P 500 stock index, which has gained about 23%.
            output: Adobe shares dropped over 6% in extended trading after the software maker\'s lighter-than-expected forecast for 2024.

            Revenue grew 12% and net income increased 26% in the fiscal fourth quarter, but Adobe\'s guidance for the new fiscal year disappointed Wall Street.

            Adobe remains focused on closing the $20 billion Figma acquisition and is responding to regulators\' concerns.

            input: Eli Lilly
            is shaking up the pharmaceutical industry with a new website offering telehealth prescriptions and direct home delivery of certain drugs, including its red-hot weight loss treatment Zepbound, to expand patient access. 

            The company’s direct-to-consumer push announced Thursday, the first of its kind for a big drugmaker, won’t necessarily upend the pharmaceutical industry and the prescription drug supply chain alone, according to some analysts.

            But other drugmakers could follow suit with their own direct-to-consumer models, according to some analysts. That could add more pressure on what many critics call a complex system for distributing, pricing and prescribing drugs in the U.S. — a structure they say has led to higher prices and fewer choices for patients.

            “There’s always a possibility for disruption. I think you should never rule out any sort of disruption,” BMO Capital Markets analyst Evan Seigerman told CNBC. “I don’t think that is necessarily happening tomorrow, but I think that you should never assume that things can’t change.”

            Lilly’s new platform comes as other companies move to disrupt the drug system in some way, in part as they face more political pressure to cut consumer costs and increase pricing transparency.

            Those actions come as lawmakers target drug supply chain middlemen in new legislation and as the Biden administration takes its own steps to rein in prices of medications, such as by giving Medicare the power to negotiate down drug prices for the first time in its six-decade history.

            Eli Lilly said its new effort — dubbed LillyDirect — aims to increase access to medicines for chronic diseases, including the highly popular weight loss drugs. 

            Those treatments, which have soared in demand over the last year as they help patients shed unwanted pounds, are plagued by supply constraints and concerns about potentially harmful knockoffs. Patients also face long waitlists to meet with obesity medicine specialists who can prescribe the drugs to them, a problem Eli Lilly hopes to address, according to Seigerman.

            Eli Lilly’s Zepbound won Food and Drug Administration approval just two months ago, but some analysts say it could garner more than $1 billion in sales in its first year on the market.

            LillyDirect won’t significantly disrupt the industry
            Eli Lilly’s site eliminates the need for a patient to visit the doctor’s office to get a prescription and, in some cases, for a pharmacy to fill it. 

            But some analysts said Eli Lilly’s site alone will not significantly threaten the traditional drug distribution system, which involves a multitiered network of manufacturers, drug wholesalers, pharmacies and pharmacy benefit managers, or PBMs.

            “I don’t think PBMs and the whole infrastructure that we have are going anywhere,” Seigerman told CNBC. “I think what [Eli Lilly] really did was identify some friction points in getting these products [weight loss drugs] to patients, and they’re coming up with a way to solve for that.” 

            “From my understanding, it’s just that there’s no retail pharmacy where a patient is having to go hunt for that particular [drug] dose, it’s being shipped right to them,” he said of Eli Lilly’s services.

            Eli Lilly’s site connects patients with an independent telehealth provider who can prescribe any FDA-approved weight loss drug or other medications for diabetes and migraines. If the prescribed treatment is Eli Lilly’s, the patient can have a third-party online pharmacy deliver it to their door. 

            Patients will also receive Eli Lilly’s discounts for drugs if they qualify for the company’s savings-card programs, the company noted in a release. One program allows people with insurance coverage for Zepbound, which costs more than $1,000 per month, to pay as little as $25 out-of-pocket. Meanwhile, those whose insurance does not cover the drug may be able to pay as low as $550.

            Some experts view that transparent pricing as a shot across the bow to PBMs, the largest of which are owned by CVS
            , UnitedHealth Group
            and Cigna
            .

            Drugmakers have long complained that they give PBMs steep drug discounts in exchange for higher placement on a formulary — an insurance plan’s list of preferred medications — only for those middlemen to not pass along savings to patients. 

            But Eli Lilly’s savings-card program and new site won’t cut PBMs out of the equation.

            “If you still use your health insurance to get these drugs through [Eli Lilly’s] website, it’s still going to get processed by a PBM,” Jeff Jonas, a Gabelli Funds portfolio manager, told CNBC.

            Patients who get drugs such as Zepbound from Eli Lilly’s site can choose to pay with cash to avoid PBMs altogether. But Bernstein analysts said in a Thursday note that they expect the “vast majority” of potential weight loss drug users to get medications through insurance. 

            Other drugmakers could follow Eli Lilly
            More pharmaceutical companies could adopt a similar approach to Eli Lilly’s.  

            Cantor Fitzgerald analyst Louise Chen said drugmakers could benefit the most from using a direct-to-consumer pharmacy model for high-selling drugs.

            “Cause of the scale of your effort, it [would] probably make sense for bigger drugs,” Chen wrote in an email to CNBC. “You get more bang for the buck and you are reaching more people.”

            But Chen said it may be more difficult for a drugmaker to pursue a direct-to-consumer model with smaller, more specialized drugs, such as treatments for complex, chronic, or rare medical conditions. For example, some drugs require specialized training for administration, such as injecting or infusing a therapy into a patient’s vein through an IV. 

            Drugmakers that do adopt a direct-to-consumer approach could add even more pressure on the nation’s traditional drug supply chain after other companies moved to simplify the system in recent months.

            That includes CVS Health
            , which announced plans to overhaul its business model for pricing prescription drugs in December, adopting a model similar to billionaire Mark Cuban’s direct-to-consumer pharmacy, Cost Plus Drugs. Health-care giant Cigna also announced in November that its PBM will offer a pricing model similar to Cuban’s venture.

            Cost Plus Drugs aims to drive down the price of medicines broadly by selling them at a set 15% markup over their cost, plus pharmacy fees.

            That company is already shaking up the broader health-care industry: CVS suffered a blow over the summer when a major California health insurer, Blue Shield of California, announced it will no longer use the company as its PBM and instead will partner with several other businesses, including Cuban’s firm and Amazon Pharmacy. 
            output: Eli Lilly launches a new website offering telehealth prescriptions and direct home delivery of certain drugs, including its weight loss treatment Zepbound.

            The move aims to increase patient access to medicines for chronic diseases and address supply constraints and concerns about potentially harmful knockoffs.

            Eli Lilly\'s direct-to-consumer approach could add pressure on the traditional drug supply chain and prompt other drugmakers to follow suit, potentially disrupting the current system for distributing, pricing, and prescribing drugs in the U.S.

            input: Apple
            shares slid less than 1% on Friday after The New York Times reported that the U.S. Department of Justice is preparing an antitrust lawsuit against the iPhone maker, which could be filed as soon as this year.

            The agency’s lawsuit could target how the Apple Watch works exclusively with the iPhone, as well as the company’s iMessage service, which is also solely available on Apple devices. It could also focus on Apple Pay, the company’s payments system, according to the report.

            The lawsuit, if it comes to pass, would be the biggest antitrust risk for Apple in years. The U.S. is Apple’s largest market, and Apple says the way in which iMessage and the Apple Watch work are essential features that distinguish iPhones from Android phones.

            The news comes as investors and analysts have started to fret about the various regulatory risks facing Apple, including new regulations in Europe over the company’s App Store’s control over iPhone software distribution, as well as a recent Justice Department trial targeting Google’s search deals, including its lucrative arrangement with Apple.

            “While Apple’s share price increased by 48% in 2023, our concerns regarding Apple’s legal risks have intensified in recent months,” CFRA analyst Nick Rodelli wrote in a note Friday.

            Apple CEO Tim Cook will meet with the European Commission’s top antitrust enforcer, Margrethe Vestager, next Thursday.

            A representative for Apple declined to comment. The Department of Justice did not immediately respond to CNBC’s requests for comment.
            output: The New York Times reported that the U.S. Department of Justice is preparing an antitrust lawsuit against Apple.

            The lawsuit could target the exclusivity of the Apple Watch and iMessage to Apple devices, as well as Apple Pay.

            This would be the biggest antitrust risk for Apple in years, as the U.S. is its largest market.

            Investors and analysts are concerned about the various regulatory risks facing Apple, including new regulations in Europe and a recent Justice Department trial targeting Google\'s search deals.

            input: {prompt}

            output: 
            """,
                **parameters
            )        

            clean_text = ' '.join(response.text.split())
            
            st.markdown(f"**Summary:** {clean_text}", unsafe_allow_html=True) 

            st.markdown(f"[Read more on this topic]({article.link})") 


if __name__ == "__main__":
    run()
