require 'rubygems'
require 'json'
require 'oauth'

class Twitterer
  attr_accessor :username
  attr_accessor :password
  
  @@baseurl = "https://api.twitter.com"	
  @@consumer_key = OAuth::Consumer.new(
	"UgswaHbTZF36PH6znsh9PkPGM",
	"NyIOHcFouZjiKMayU7DWrKjxw817nCtSu213NGpXDvWrdZqKP6")
  @@access_token = OAuth::Token.new(
	"2415395470-diHLjzbI441ypGqGweKK5bbfD82G7cSYh5zpJVl",
	"nrGV3uRX9MHYDzOwrI3wEhH5yBd1ffrMPUvfEYIGTx1Ho")

  # Create the object
  def initialize()
    @username = "buzzwordipsum"
	@password = "passw0rd"
	
  end
  
  # Print data about a Tweet
	def print_tweet()
		path    = "/1.1/statuses/show.json"
		query   = URI.encode_www_form("id" => "266270116780576768")
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
	
	# Sends a tweet
	def sendTweet(message)
		path = "/1.1/statuses/update.json"
		query = URI.encode_www_form("status" => message)
		address = URI("#{@@baseurl}#{path}")
		
		request = Net::HTTP::Post.new address.request_uri
		request.set_form_data("status" => "Hello, business world!")
		
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
		request.oauth! http, @@consumer_key, @@access_token
		http.start
		response = http.request request
	end

end

if __FILE__ == $0
	twitterer = Twitterer.new
	puts twitterer.username  

	puts twitterer.print_tweet
	
	puts "now trying to send a tweet..."
	twitterer.sendTweet("Hello, Business World!");
	puts "done?"
	
end