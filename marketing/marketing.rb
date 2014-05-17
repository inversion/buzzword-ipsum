require 'rubygems'

require 'yaml'
require 'json'
require 'oauth'

YAML_FILE = "./twitter_user.yml"

class Twitterer
  
  @@baseurl = "https://api.twitter.com"	

  # Create the object
  def initialize()
	loadUserProperties    
  end
  
  def loadUserProperties()
    properties = YAML.load_file(YAML_FILE)
	
	@consumer_key = OAuth::Consumer.new(
		properties["apikey"],
		properties["apisecret"]
	)
	@access_token = OAuth::Token.new(
		properties["accesstoken"],
		properties["accesssecret"]
	)
	
  end
  
  # Print data about a Tweet
	def print_tweet(id)
		path    = "/1.1/statuses/show.json"
		query   = URI.encode_www_form("id" => id)
		address = URI("#{@@baseurl}#{path}?#{query}")
		
		request = Net::HTTP::Get.new address.request_uri

		# Set up HTTP.
		http = setupHTTP(address)		
		response = sendRequest(request, http)

		# Parse and print the Tweet if the response code was 200
		tweet = nil
		if response.code == '200' then
		  tweet = JSON.parse(response.body)
		  pretty_print_tweet(tweet)
		end
	end
	
	#Get a list of the account's followers
	def getFollowers
		path = "/1.1/followers/list.json"
		query = URI.encode_www_form("screen_name" => "BuzzwordIpsum")
		address = URI("#{@@baseurl}#{path}?#{query}")
		
		request = Net::HTTP::Get.new address.request_uri
		
		http=setupHTTP(address)
		response = sendRequest(request, http)
		
		if response.code == '200' then
			users = JSON.parse(response.body)			
			return users["users"]
		end
	end
	
	def getRandomFollowerName(users)
		selection = rand(0...users.length) #i.e. 0..numusers - 1
		return users[selection]["screen_name"]
	end
	
	# Sends a tweet
	def sendTweet(message)
		path = "/1.1/statuses/update.json"
		address = URI("#{@@baseurl}#{path}")
		
		request = Net::HTTP::Post.new address.request_uri
		request.set_form_data("status" => message)
		
		# Set up HTTP.
		http = setupHTTP(address)
		response = sendRequest(request, http)
		
		if response.code == '200' then
			tweet = JSON.parse(response.body)
			puts "Successfully sent tweet: #{tweet["text"]}"
		else
			puts "Could not send tweet: " + "Code: #{response.code} Body: #{response.body}"
		end
	end
	
	def pretty_print_tweet(tweet)
		puts tweet["user"]["name"] + " - " + tweet["text"]
	end
	
	def setupHTTP(address)
		http             = Net::HTTP.new address.host, address.port
		http.use_ssl     = true
		http.verify_mode = OpenSSL::SSL::VERIFY_NONE
		return http
	end
	
	def sendRequest(request, http)
		request.oauth! http, @consumer_key, @access_token
		http.start
		response = http.request request
	end
end

class Buzzworder
	@@baseurl = "http://www.buzzwordipsum.com"	

  # Create the object
  def initialize()
	    
  end
  
  def setupHTTP(address)
	http             = Net::HTTP.new address.host, address.port
	return http
  end
  
  def getParagraph(type = "sentences")
	path    = "/buzzwords"
	query   = URI.encode_www_form("type" => type)
	address = URI("#{@@baseurl}#{path}?#{query}")
	#address = URI("#{@@baseurl}#{path}")
	
	request = Net::HTTP::Get.new address.request_uri

	# Set up HTTP.
	http = setupHTTP(address)		
	http.start
	response = http.request request
	
	return response.body		
   end
   
   def getSentence()   
		para = getParagraph()
		#given a paragraph, find a sentence that's < 144 characters - i.e. loop until EOF
		sentenceRegex = /[^(\. )].*?[\.\?]/ 
		
		results = para.scan(sentenceRegex)
		results.each do |result|
			if result.length <= 140
				#one in 4 times, add a hash tag to the end of the message (if it'll fit)
				if rand(0..3) == 0
					potentialHashtag = " " + getHashtag
					if (result.length + potentialHashtag.length <= 140)
						result = result + potentialHashtag
					end
				end
				
				return result
			end
		end
		return "No strings less than 140 characters. Try again!"
   end
   
   def getHashtag
		para = getParagraph("words")
		#pick a word, any word (well, okay, it'll be the second word. but it's random so shhhh)
		wordRegex = / (.*?) /
		match = wordRegex.match(para).captures[0]
		return "#" + match
   end
   
end

#I name my classes what I want
class SleepyBuzzworder
	
	def synergise
		loop do
			tweetBuzzword
			minuteOffset = (-10 + rand(20)) * 60
			delay = 1 * 60 * 60 + minuteOffset
			puts "Sleeping for: #{delay.div(60*60)} hours, #{delay.div(60) % 60} minutes"
			sleep(delay) #sleep an hour or so
			puts "I'm back!"
		end
	end
end

def tweetBuzzword
	buzzworder = Buzzworder.new
	sentence = ""
	loop do
		sentence = buzzworder.getSentence
		break if (sentence != "No strings less than 140 characters. Try again!" && sentence != "")
	end
	twitterer = Twitterer.new
	twitterer.sendTweet(sentence)	
	
	return sentence
end

def printUsage
	puts "Usage: marketing.rb {tweet message}/{buzzwords}/{automatedBuzzwordify}/{follower}"
end

case ARGV[0]
when "tweet"
	twitterer = Twitterer.new
	ARGV[1].nil? ? printUsage : twitterer.sendTweet(ARGV[1])
when "buzzwords"
	tweetBuzzword
when "automatedBuzzwordify"
	sleepy = SleepyBuzzworder.new
	sleepy.synergise #permanent loop
when "follower"
	twitterer = Twitterer.new
	fo = twitterer.getFollowers
	puts twitterer.getRandomFollowerName(fo)
else 
	printUsage
end
