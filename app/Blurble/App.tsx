import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { 
  StyleSheet, 
  Text,
  View, 
  TextInput, 
  Dimensions, 
  ScrollView 
} from 'react-native';

export default function App() {
  const [title, setTitle] = React.useState('')
  const [content, setContent] = React.useState('')

  return (
    <View style={styles.container}>
      <View style={styles.inputView}>
        <TextInput
          style={styles.titleInput}
          placeholder="Title"
          onChangeText={(newTitle: React.SetStateAction<string>) => setTitle(newTitle)}
          defaultValue={title}
        />

        <TextInput
          style={styles.contentInput}
          placeholder="Blurb"
          onChangeText={(newContent: React.SetStateAction<string>) => setContent(newContent)}
          defaultValue={content}
        />
      </View>
      <View style={styles.resultsView}>
        <ScrollView>
          <Text>Open up App.tsx to start working on your app!</Text>
          <Text style={{fontSize: 60}}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
            minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat. Duis aute irure dolor in
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
            culpa qui officia deserunt mollit anim id est laborum.
          </Text>
        </ScrollView>  
      </View>
      <StatusBar style="auto" />
    </View>
  );
}

const deviceWidth = Dimensions.get('window').width;
const deviceHeight = Dimensions.get('window').height;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    marginTop: deviceHeight * 0.1,
    marginBottom: deviceHeight * 0.03,
    marginLeft:  deviceWidth * 0.02,
    marginRight: deviceWidth * 0.02,
  },
  inputView: {
    flex: 0.1,
    backgroundColor: 'blue',
    alignItems: 'flex-start',
  },
  resultsView: {
    flex: 0.9,
    backgroundColor: 'red',
  },
  titleInput: {
    height: '40px',
    width: 200,
    fontSize: 30,
    textAlign: 'left',
    borderWidth: 1,
  },
  contentInput: {
    height: '40px',
    fontSize: 20,
  }
});
