import csv

# Sample paragraph
paragraph = """
Dubai’s economy has grown 11-fold between 1975 and 2008
rendering it the fastest-growing economy in the world over
the same period. During the past two decades, numerous
strategic ICT and digital transformation initiatives in the city
has altered and digitised various aspects of life. Dubai incorporates ‘smart design’ into its fabric and has been able to fuse
cyber and physical infrastructure and systems while rapidly
expanding to accommodate the next projected 30 million
visitors by 2020.
Dubai has already achieved world-class leading city status
with respect to various SDG 11 indicators as highlighted below.
Housing: No one lives in slums, and there are no homeless or informal settlements in Dubai. All households have
registered titles.
Access to basic services: Dubai has achieved 100 per
cent potable water supply and authorized electrical service,
100 per cent sustainable access to improved water source,
and 100 per cent of the population has access to sanitation
facilities as well as wastewater collection and treatment. The
UAE, represented by Dubai utilities DEWA, maintained its
first place globally, for the second consecutive year in all of
the Getting Electricity indicators in the World Bank’s Doing
Business 2019 report.
The city’s population has access to healthcare facilities.
And Dubai is well known as one of the safest cities in the
world. 100 per cent of the population has completed primary
education, and the secondary and tertiary education rates
are high.
Access to Transport: Dubai with its high income and high
GDP per capita status also has a high percentage of private
vehicle ownership, a well-established modern multi-modal
transport infrastructure on sea, land and air with an extensive public transport network, and is currently expanding its
bicycle routes substantially across the city.
Inclusive and sustainable urbanization: Dubai has a relatively low population density, a high female participation rate
in the workforce and a long term urban plan.
Environment and resilience: Dubai has had no natural
disaster related deaths. It has 100 per cent regular solid waste
collection. Dubai has achieved competitive results, surpassing major European and American utilities in efficiency and
reliability; electricity transmission and distribution networks
losses were reduced to 3.3 per cent compared to 6–7 per
cent in the US and Europe, while water network losses were
reduced to 6.6 per cent compared to 15 per cent in the US,
which is one of the best results in the world. Dubai has also
achieved one of the lowest records of customer minutes lost
per year (CML) in the world — 2.39 CML compared to 15
minutes in Europe. 
"""

# Splitting the paragraph into sentences
sentences = paragraph.strip().split('.')

# Removing empty entries and stripping whitespace
sentences = [sentence.strip() for sentence in sentences if sentence]

# Specify the CSV file name
filename = "sentences.csv"

# Writing to CSV
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sentence'])
    for sentence in sentences:
        writer.writerow([sentence])

print(f"Sentences have been written to {filename}")
