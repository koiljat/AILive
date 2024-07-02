import React from 'react';
import {
  StyleSheet,
  TouchableOpacity,
  View,
  SafeAreaView,
  Text,
  Alert,
  Image
} from 'react-native';

export default function Tiktok() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={styles.button}
          onPress={() => Alert.alert('Button pressed')}
        >
          <Text style={styles.buttonText}>Generate</Text>
        </TouchableOpacity>
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
    top: '20%',  
    left: 0,
    right: 0,
    alignItems: 'center',  
  },
  button: {
    backgroundColor: 'rgba(255, 105, 100, 0.8)',  
    padding: 15,
    borderRadius: 20,  
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',  
    fontSize: 16,
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
