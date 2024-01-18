import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { Button, View, Text, Animated, StyleSheet, ImageBackground, FlatList, TouchableOpacity } from 'react-native';
import { createDrawerNavigator, DrawerContentScrollView, DrawerItemList, DrawerItem } from '@react-navigation/drawer';
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import {
  LineChart,
  BarChart,
  PieChart,
  ProgressChart,
  ContributionGraph,
  StackedBarChart,
} from 'react-native-chart-kit';





const MyBezierLineChart = ({data}) => {
  return (
    <>
      <Text style={styles.header}></Text>
      <LineChart
        data={{
          labels: data.lbl,
          datasets: [
            {
              data: data.d,
            },
          ],
        }}
        width={150} // from react-native
        height={220}
        yAxisLabel={'Rs'}
        chartConfig={{
          backgroundColor: '#1cc910',
          backgroundGradientFrom: '#eff3ff',
          backgroundGradientTo: '#efefef',
          decimalPlaces: 2, // optional, defaults to 2dp
          color: (opacity = 255) => `rgba(0, 0, 0, ${opacity})`,
          style: {
            borderRadius: 30,
          },
        }}
        bezier
        style={{
          marginVertical: 80,
          borderRadius: 16,
        }}
      />
    </>
  );
};


const Page = ({ title,data }) => (
  <View style={styles.pageContainer}>
    <MyBezierLineChart data={data} />
    <Text style={styles.pageText}>{title}</Text>
  </View>
);

const StatData = ({ route }) => {
  const { title, data } = route.params;
  
  return (
    <Page title={title} data={data} />
  );
};


const TypewriterText = ({ texts, delay }) => {
  const [currentText, setCurrentText] = useState(0);
  const [typedText, setTypedText] = useState('');

  useEffect(() => {
    const textInterval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * texts.length);
      const selectedText = texts[randomIndex];
      const words = selectedText.split(' ');

      let currentWordIndex = 0;

      const typingInterval = setInterval(() => {
        if (currentWordIndex < words.length) {
          setTypedText((prevText) => prevText + words[currentWordIndex] + ' ');
          currentWordIndex++;
        } else {
          clearInterval(typingInterval);
          setTimeout(() => {
            setTypedText('');
            setCurrentText('');
          }, delay);
        }
      }, delay);
      setCurrentText(selectedText);

      return () => {
        clearInterval(typingInterval);
      };
    }, delay * (currentText.length + 1));

    return () => {
      clearInterval(textInterval);
    };
  }, [texts, delay, currentText]);

  return (
    <Text style={styles.text}>
      {typedText}
    </Text>
  );
};

const HomeScreen = ({ navigation }) => {
  const texts = ['Health-Hactivists', 'Wellness', 'Fitness', 'Nutrition', 'Exercise', 'Healthy', 'Balance', 'Diet', 'Hydration', 'Strength', 'Flexibility', 'Endurance', 'Cardio', 'Weight', 'Vitamins', 'Minerals', 'Protein', 'Fiber', 'Calcium', 'Iron', 'Antioxidants', 'Superfoods', 'Organic', 'Whole Foods', 'Plant-based', 'Low Carb', 'Low Fat', 'Sugar-Free', 'Gluten-Free', 'Allergies', 'Immunity', 'Wellbeing', 'Mental Health', 'Stress', 'Anxiety', 'Depression', 'Self-care', 'Sleep', 'Rest', 'Relaxation', 'Meditation', 'Yoga', 'Mindfulness', 'Happiness', 'Positive', 'Emotional', 'Self-esteem', 'Confidence', 'Motivation', 'Energy', 'Resilience', 'Recovery', 'Healing', 'Pain', 'Prevention', 'Screen Time', 'Posture', 'Ergonomics', 'Heart', 'Lungs', 'Brain', 'Liver', 'Kidneys', 'Digestion', 'Metabolism', 'Cholesterol', 'Blood Pressure', 'Blood Sugar', 'Cancer', 'Diabetes', 'Obesity', 'Stroke', 'Arthritis', 'Osteoporosis', 'Alzheimer\'s', 'Dementia', 'Vision', 'Hearing', 'Dental', 'Oral Hygiene', 'Skin', 'Hair', 'Nails', 'Detox', 'Cleanse', 'All-natural', 'Herbal', 'Holistic', 'Alternative Medicine', 'Physical Therapy', 'Rehabilitation', 'Wellness Coach'];

  return (
    <View style={styles.container}>
      <ImageBackground
        source={require('./home_bg.jpg')}
        style={styles.backgroundImage}
      >
        <TypewriterText texts={texts} delay={400} />
      </ImageBackground>
    </View>
  );
};






const Statistics = ({ navigation }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('https://f9d3-49-37-46-169.ngrok-free.app/statistics');
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.notificationContainer}
      onPress={() => navigation.navigate('Statistics-Sub', { title: item.title, data: item })}
    >
      <Text style={styles.notificationText}>{item.title}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={data}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};


const CustomDrawerContent = (props) => {
  const filteredItems = props.state.routeNames.filter((routeName) => routeName !== 'Error');

  return (
    <DrawerContentScrollView {...props}>
      <DrawerItemList {...props} state={{ ...props.state, routeNames: filteredItems }} />
    </DrawerContentScrollView>
  );
};

const Drawer = createDrawerNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Drawer.Navigator useLegacyImplementation initialRouteName="Home" drawerContent={CustomDrawerContent}>
        <Drawer.Screen name="Home" component={HomeScreen} />
        <Drawer.Screen name="Statistics" component={Statistics} />
        <Drawer.Screen name="Statistics-Sub" component={StatData} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#E598C2',
  },
  text: {
    fontSize: 36,
    fontWeight: 'bold',
    color: 'white',
    paddingBottom: 100,


  },
  backgroundImage: {
    flex: 1,
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContainer: {
    flexGrow: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  notificationContainer: {
    marginBottom: 12,
    backgroundColor: 'pink',
    paddingVertical: 12,
    paddingHorizontal: 100,
    borderRadius: 8,
  },
  notificationText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333333',
  },
  pageContainer: {
    flex: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: 'pink',
    
  },
  pageText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'black',
  },
  buttonContainer: {
    marginBottom: 12,
    backgroundColor: 'lightblue',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
});
