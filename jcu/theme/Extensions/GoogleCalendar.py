import urllib
import urllib2

def createGoogleCalendarEvent(self, email, password, calendar_url, start_time, end_time, title, location, content ):
	#Authenticate with Google for our given account
	auth_uri = 'https://www.google.com/accounts/ClientLogin'
	authreq_data = urllib.urlencode({ 'Email':   email,
        	                          'Passwd':  password,
                	                  "service": "cl",
                        	          "source":  "jcu-plone-1",
                                	  "accountType": "HOSTED_OR_GOOGLE" })
	auth_req = urllib2.Request(auth_uri, data=authreq_data)
	auth_resp = urllib2.urlopen(auth_req)
	auth_resp_body = auth_resp.read()
	# auth response includes several fields - we're interested in
	#  the bit after Auth=
	auth_resp_dict = dict(x.split("=")
        	              for x in auth_resp_body.split("\n") if x)
	authtoken = auth_resp_dict["Auth"]

	#Create the required headers to make Google happy
	headers = {"Authorization": 'GoogleLogin auth='+authtoken, "Content-Type": "application/atom+xml", "GData-Version": "2"}

	#Create the event body, as per the detailed entered
	eventContent = """
<entry xmlns='http://www.w3.org/2005/Atom'
    xmlns:gd='http://schemas.google.com/g/2005'>
  <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
  <title type='text'>"""+ title +"""</title>
  <content type='text'>"""+ content +"""</content>
  <gd:transparency
    value='http://schemas.google.com/g/2005#event.opaque'>
  </gd:transparency>
  <gd:eventStatus
    value='http://schemas.google.com/g/2005#event.confirmed'>
  </gd:eventStatus>
  <gd:where valueString='"""+ location +"""'></gd:where>
  <gd:when startTime='"""+ start_time +"""'
    endTime='"""+ end_time +"""'></gd:when>
</entry>
    """

	#Create and send the relevant requests
	req = urllib2.Request(calendar_url, event, headers)
	
	try:
		calresponse = urllib2.urlopen(req)

		#Google requires a 2nd request to the relevant url
		req2 = urllib2.Request(calresponse.geturl(), event, headers)
		try:
			calresponse2 = urllib2.urlopen(req2)
       		#ignore the 'error' since it actually means it worked

