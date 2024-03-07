## Approach
My approach largely focused on trying to use the information that we have in the main large file we are given rather than
downloading the zipped JSON files that are referenced from the large file. I started by using google to figure out if any
part of the EIN (such as the prefix) mapped to a specific state. From
what I could tell, there was no way to accurately link an EIN to a location. This makes sense because an employer could
employ people in multiple states. At this point I started breaking down the location urls and found that in the json
file names there were dates, some alpha-numerics, and a brief description of what the rates were. I figured that if there
was any mapping to location, it would have to be part of the alpha numeric section. While I had this hunch, I was a bit stumped
as to how those may map to location and plan type.

The thing that got me unblocked at this point was Anthem's tool for EIN lookups. When looking up an EIN from the main file,
it returns three lists -- the In-Network Negotiated Rates Files, the Out-of-Network Allowed Amounts Files, and the
Blue Cross Blue Shield Association Out-of-Area Rates Files. These lists of JSON files have state codes within the file name
such as 2024-03_NY_39B0_in-network-rates_1_of_10.json.gz. When these links are hovered, you can see the alpha numeric that
the "NY_39B0" piece maps to "254_39B0". When I searched for this string in the main file I found that there were a lot of
urls that had this New York mapping.

This investigation took about an hour and then I started writing some code to isolate those URLs. To stream over all of the
~27 gigabytes I used the ijson library so that I wasn't loading all of the file in to memory. While the resulting list
of URLs have some state codes in the base URL, from what I can tell the "254" piece of the json file name maps directly to New York.
I only considered the in network urls here as from what I can tell, Highmark is a different insurance company than Anthem.
While I ran out of time for the take-home and didn't find a programmatic way to discern whether a URL is for PPO plans, after downloading some of the location
URLs I saw that the negotiation_arrangement is FFS. Fee for service is a subset of PPO so I am considering those correctly
dubbed as PPO plans.

The the description field had some valuable information but they could not be relied on entirely to find all of the Anthem
PPO providers in New York. I think that my solution is incomplete as I would like to do more research about in network
versus out of network providers and the different negotiation_arrangements. As I said in the beginning of this readme,
I was optimizing for a solution that did not have to download the location files to ascertain additional information.
This was due to the fact that I wanted the program to run quickly and avoid taking up the entire memory of my computer.
If this was a background job running in a server-less environment it would be a bit more feasible to scan those files
for additional information.

## Program Stats and Running Locally

To run this program locally you will need to download the large index file as well as install `ijson`
1) Download the file
2) Run `pip install ijson` from the python command line or `python3 -m pip install ijson` if you have python3 installed
3) Update line 58 in `file_download.py` to use the local path of the file downloaded in step 1
4) Run the program

The list of urls can be found in output.txt. When I ran the program locally I had the following stats

The program took 224.74 seconds to run.
There were 1409028 urls added to the output.
The output file size is 682414978 bytes or 650.8016376495361 MB