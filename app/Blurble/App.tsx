import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { 
  StyleSheet, 
  Text,
  View, 
  Button,
  Dimensions, 
  ScrollView,
} from 'react-native';
import { Card, Input } from 'react-native-elements';

interface Blurble {
  id: number;
  title: string;
  content: string;
  datetime: string;
}

/**
 * Get the width and height of the device screen 
 * and make available globally.
 */
const DEVICE_WIDTH = Dimensions.get('window').width;
const DEVICE_HEIGHT = Dimensions.get('window').height;

const HOST_ADDR: string = 'http://localhost:5000/';


export default function App() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [blurbles, setBlurbles] = useState<Blurble[]>([]);

  /**
   * Sends a Blurble to the API, which stores it in the 
   * database. After we've successfully stored the Blurble,
   * fetch all Blurbles from the database to update
   * our state.
   * @returns void
   * @throws {Error} Error if the API call fails
   */
  const sendBlurble = async () => {
    try {
      const response = await fetch(HOST_ADDR + 'insert', {
        method: 'POST',
        headers: {
          // Note the CORS wildcard here.
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          content: content,
        }),
      });
    } catch (error) {
      console.error(error);
    } finally {
      await getBlurbles();
    }
  }

  /**
   * Asynchronously fetches a blurble from the API
   * at the designated endpoint.
   * @returns {object} A json object containing a list of Blurbles
   * @throws {Error} If the request fails
   */
  const getBlurbles = async () => {
    try {
        // CORS is disabled for development purposes,
        // however set your needs accordingly for production.
        const response = await fetch(`${HOST_ADDR}`);
        const json = await response.json();
        setBlurbles(json);
    } catch (error) {
        console.error(error);
    } finally {
      return blurbles;
    }
  };

  useEffect(() => {
    getBlurbles();
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.inputView}>
        <Input
          style={styles.titleInput}
          label="Title"
          labelStyle={styles.titleLabel}
          placeholder="What a day..."
          onChangeText={(newTitle: React.SetStateAction<string>) => setTitle(newTitle)}
          defaultValue={title}
        />

        <Input
          style={styles.contentInput}
          label="Blurble"
          labelStyle={styles.contentLabel}
          placeholder="First I woke up, then I ate, then..."
          onChangeText={(newContent: React.SetStateAction<string>) => setContent(newContent)}
          defaultValue={content}
        />

        <Button
          onPress={sendBlurble}
          title="Send Blurble"
        />
      </View>
      <View style={styles.resultsView}>
        <ScrollView>
          {blurbles.map(function(item, index) {
            return (
              <Blurble 
                key={index} 
                id={item.id} 
                title={item.title} 
                content={item.content} 
                datetime={item.datetime} 
              />
            )
          })}
        </ScrollView>  
      </View>
      <StatusBar style="auto" />
    </View>
  );
}

export function Blurble(props: Blurble) {
  return (
    <View>
      <Card>
        <Card.Title>{props.title}</Card.Title>
        <Card.Divider />
        <Text>{props.content}</Text>
        <Text>{props.datetime}</Text>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    marginTop: DEVICE_HEIGHT * 0.1,
    marginBottom: DEVICE_HEIGHT * 0.03,
    marginLeft:  DEVICE_WIDTH * 0.02,
    marginRight: DEVICE_WIDTH * 0.02,
  },
  inputView: {
    flex: 0.2,
    alignItems: 'stretch',
  },
  resultsView: {
    flex: 0.8,
  },
  titleInput: {
    fontSize: 40,
    textAlign: 'left',
  },
  titleLabel: {
    fontSize: 30,
  },
  contentInput: {
    flex: 1,
    fontSize: 20,
  },
  contentLabel: {
    fontSize: 20,
  }
});
