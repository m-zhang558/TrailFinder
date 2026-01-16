import React, { Component } from 'react';
import MapScreen from './frontend/Map'
// import { StyleSheet, Text, View } from 'react-native';

export default class App extends Component {
    render() {
        return (
            <MapScreen/>
            /*<View style={styles.container}>
                <Text style={styles.text}>TrailFinder</Text>
            </View>*/
        );
    }
}

/*const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        color: 'red'
    },
});*/