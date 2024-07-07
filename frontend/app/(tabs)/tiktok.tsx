import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  TouchableOpacity,
  View,
  Text,
  ImageBackground
} from 'react-native';

export default function Home() {
  const [buttonColor, setButtonColor] = useState('rgba(255, 105, 100, 0.8)');
  const [showText, setShowText] = useState(false);
  const [summary, setSummary] = useState('');
  const [sentimentColor, setSentimentColor] = useState('green'); 

  const toggleTextVisibility = () => {
    setShowText(!showText);
    setButtonColor(showText ? 'rgba(255, 105, 100, 0.8)' : 'rgba(147, 58, 55, 0.8)');
  };

  const updateSentimentColor = (sentimentSummary: string) => {
    if (sentimentSummary.includes('NEGATIVE')) {
      setSentimentColor('red');
    } else {
      setSentimentColor('green');
    }
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
  
  useEffect(() => {
    fetchSummary();

    // Fetch summary every minute
    const interval = setInterval(() => {
      fetchSummary();
    }, 60000); 

    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <ImageBackground source={require('@/assets/images/tiktok-live.jpeg')} style={styles.image}>
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
    justifyContent: 'center',
  },
  buttonContainer: {
    position: 'absolute',
    zIndex: 1,
    top: '10%',
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
    backgroundColor: 'rgba(255, 255, 255, 0.9)', 
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
    top: '10%',
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
});
