import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  TouchableOpacity,
  View,
  Text,
  ScrollView,
  SafeAreaView,
  ImageBackground
} from 'react-native';

export default function Home() {
  const [buttonColor, setButtonColor] = useState('rgba(255, 105, 100, 0.8)');
  const [showText, setShowText] = useState(false);
  const [summary, setSummary] = useState('');
  const [sentimentColor, setSentimentColor] = useState('green');
  const [chatMessage, setChatMessage] = useState([]);
  const scrollViewRef = useRef();

  const toggleTextVisibility = () => {
    setShowText(!showText);
    setButtonColor(showText ? 'rgba(255, 105, 100, 0.8)' : 'rgba(147, 58, 55, 0.8)');
  };

  const updateSentimentColor = (sentimentSummary) => {
    const lines = sentimentSummary.trim().split('\n');
    let positiveCount = 0;
    let negativeCount = 0;
  
    lines.forEach(line => {
      if (line.includes('Sentiment: POSITIVE')) {
        positiveCount++;
      } else if (line.includes('Sentiment: NEGATIVE')) {
        negativeCount++;
      }
    });
  
    const majorityColor = positiveCount + 3 > negativeCount ? 'green' : 'red';
    setSentimentColor(majorityColor);
    console.log(`Positive count: ${positiveCount}, Negative count: ${negativeCount}`);
  };
  

  const fetchSummary = () => {
    fetch('http://localhost:5001/summary')
      .then(response => response.json())
      .then(data => {
        setSummary(data.summary);
        updateSentimentColor(data.aspect_sentiment_summary);
      })
      .catch(error => {
        console.error('Error fetching summary:', error);
      });
  };

  const fetchChatMessage = () => {
    fetch('http://localhost:5001/getChat')
      .then(response => response.json())
      .then(data => {
        setChatMessage(data.chat);
        // Scroll to the bottom of the ScrollView
        if (scrollViewRef.current) {
          scrollViewRef.current.scrollToEnd({ animated: true });
        }
      })
      .catch(error => {
        console.error('Error fetching chat message:', error);
      });
  };

  useEffect(() => {
    fetchSummary();
    fetchChatMessage();

    // Fetch summary every minute
    const summaryInterval = setInterval(fetchSummary, 6000);

    // Fetch chat messages every 0.6 seconds
    const chatInterval = setInterval(fetchChatMessage, 600);

    return () => {
      clearInterval(summaryInterval);
      clearInterval(chatInterval);
    };
  }, []);

  return (
    <View style={styles.container}>
      <ImageBackground source={require('@/assets/images/shoe.jpeg')} style={styles.image}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, { backgroundColor: buttonColor }]}
            onPress={toggleTextVisibility}
          >
            <Text style={styles.buttonText}>Generate</Text>
          </TouchableOpacity>
          {showText && (
            <View style={styles.hiddenTextContainer}>
              <Text style={styles.hiddenText}>{summary}</Text>
            </View>
          )}
        </View>
        <View style={[styles.sentimentBubble, { backgroundColor: sentimentColor }]} />
        <View style={[{ height: 200, top: 550 }]}>
          <ScrollView
            ref={scrollViewRef}
            contentContainerStyle={styles.chatContainer}
            onContentSizeChange={() => scrollViewRef.current.scrollToEnd({ animated: true })}
          >
            {chatMessage.map((item, index) => (
              <Text key={index} style={styles.chatMessage}>
                {item.message}
              </Text>
            ))}
          </ScrollView>
        </View>
      </ImageBackground>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  image: {
    flex: 1,
  },
  buttonContainer: {
    position: 'absolute',
    zIndex: 1,
    top: '5%',
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  button: {
    padding: 15,
    borderRadius: 20,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
  hiddenTextContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.7)',
    margin: 10,
    borderRadius: 10,
    marginTop: 10,
  },
  hiddenText: {
    fontSize: 16,
    color: 'black',
    borderWidth: 1,
    padding: 10,
    borderRadius: 5,
  },
  sentimentBubble: {
    position: 'absolute',
    zIndex: 1,
    top: '5%',
    left: '15%',
    right: 0,
    alignItems: 'center',
    flexDirection: 'column',
    justifyContent: 'center',
    width: 40,
    height: 40,
    borderRadius: 20,
    marginLeft: 10,
    borderWidth: 1,
    borderColor: 'black',
  },
  chatContainer: {
    flexGrow: 1,
    marginHorizontal: 10,
    marginBottom: 10,
    paddingHorizontal: 10,
    paddingVertical: 5,
    backgroundColor: 'rgba(255, 255, 255, 0.5)',
    borderRadius: 10,
    alignItems: 'flex-start'
  },
  chatMessage: {
    fontSize: 16,
    paddingVertical: 5,
  },
});