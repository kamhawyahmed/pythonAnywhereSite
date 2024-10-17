#IDEAS - 
# Boldly display phone number and "Text in 'patient' or 'provider' any time to the phone number above to begin." - DONE
#simulate virtual phone receiving and sending (either real to p# or simulated shown on website) messages
#simulate database updating live with each entry
#simulate online emr looking webpage for internet-based entry


#need db backend
#need text messaging backend
#need text messaging workflow patient updates and check-ins
#need text messaging workflow provider data input
#need openai backend summarizing and reformatting info

#need virtual phone frontend w/ text animations
#need db frontend (excel looking format)
#need emr simulated online input form
#buttons to cycle from virtual phone 

import Twilio
print(Twilio.fetch_messages_to_list())