import React, { useState } from 'react';
import {
  StyleSheet,
  TouchableOpacity,
  View,
  SafeAreaView,
  Text,
  Image
} from 'react-native';

export default function Tiktok() {
  const [buttonColor, setButtonColor] = useState('rgba(255, 105, 100, 0.8)');
  const [showText, setShowText] = useState(false);

  const toggleTextVisibility = () => {
    setShowText(!showText);
    setButtonColor(showText ? 'rgba(255, 105, 100, 0.8)' : 'rgba(147, 58, 55, 0.8)');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, { backgroundColor: buttonColor }]}
          onPress={toggleTextVisibility}
        >
          <Text style={styles.buttonText}>Generate</Text>
        </TouchableOpacity>
        {showText && (
          <View style={styles.hiddenTextContainer}>
            <Text style={styles.hiddenText}>In the heart of the bustling city, amid the cacophony of honking horns and hurried footsteps, stood a quaint little bookstore with weathered wooden shelves that stretched from floor to ceiling, each shelf laden with a myriad of books in various stages of use. The air inside was thick with the comforting scent of aged paper and ink, mingling with the faint aroma of freshly brewed coffee from a small corner café tucked at the back. The bookstore's windows, adorned with faded lace curtains that swayed gently in the breeze, offered a glimpse into a world frozen in time. Passersby, enticed by the charm of its vintage facade, often found themselves drawn to its threshold, curious to explore its treasures. Inside, soft jazz music played softly from a hidden corner, where a vintage record player spun melodies of forgotten years. The walls, painted a warm, inviting shade of ochre, were lined with literary treasures both ancient and modern, their spines forming a mosaic of genres and authors. Each book whispered stories of love, adventure, and mystery, their pages worn smooth by the hands of countless readers who had journeyed through their pages.</Text>
          </View>
        )}
      </View>
      <View style={styles.imageContainer}>
        <Image source={require('@/assets/images/tiktok-live.jpeg')} style={styles.image} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
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
  imageContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: '100%',
    height: 900,
    resizeMode: 'cover',
  },
});
