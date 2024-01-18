# ECG Cloud Project Readme

## Overview

🌐 Welcome to the ECG Cloud Project! This project utilizes Azure services for end-to-end management of ECG data. It involves collecting data from an IoT device through Azure IoT Hub, processing the data using Azure Stream Analytics, storing it in a SQL database, and visualizing patient details through a Django CRM. Additionally, machine learning is applied to convert the data to a 12-lead ECG format. The project includes a React Native app for mobile access.
![Frame 1 (1)](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/c89f0c00-556c-4abd-9894-76676cf86900)

## Project Components

🔧 **IoT Data Collection:**
   - ECG data from three leads is collected from an IoT device via Azure IoT Hub.
   ![Frame 4 (4)](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/643d09c8-ee3c-493c-8022-78cde130505c)
   The IoT Device
   - The Device gets connected to wifi and send three lead ECG data to the Azure Cloud
   ![3-Lead-ECG-a-Lead-I-b-Lead-II-c-Lead-III](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/df56225f-707e-4615-b042-3da58a262da6)
   The Three Lead ECG Data

🌊 **Stream Analytics:**

🗃️ **SQL Database:**

🌐 **Django CRM:**

⚙️ **Machine Learning:**
   - Machine learning algorithms are applied to convert the collected data into a 12-lead ECG format for comprehensive analysis.

📱 **React Native App:**

☁️ **Azure VM Hosting:**
![image](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/0c7e7866-1637-499e-95bc-4dd533d2e921)

   


## Getting Started

1. **Azure Setup:**
   - Ensure you have an active Azure subscription.
   - Create an Azure IoT Hub, Stream Analytics job, SQL database, and a Virtual Machine for hosting Django and React Native.
   
![image](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/83ee9900-1f9d-4825-98c2-7e3a66dfe330)
![image](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/f1f53ba1-d565-4fcf-98b8-55ce9ae5b196)
![image](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/81e3db10-d347-43e0-9c42-ad60a1836836)
![image](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/3d28ac4d-7b5d-4016-845d-b20e4b50edbc)





2. **IoT Device Integration:**
   - Connect your IoT device to Azure IoT Hub using the provided connection string.

3. **Stream Analytics Configuration:**
   - Configure Azure Stream Analytics to process incoming data from IoT Hub and store it in the SQL database.

5. **Machine Learning:**
   ![12911_2023_2233_Fig1_HTML](https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/f90a11a5-6914-41f0-965d-6bd612d403fc)
   THE PREDICTED 12 LEAD ECG GRAPH   

7. **Azure VM Hosting:**
   - Deploy the Django CRM and React Native app on the Azure Virtual Machine.

8. **Testing:**
   - Test the end-to-end flow: IoT data collection, Stream Analytics processing, SQL database storage, Django CRM access, machine learning conversion, and React Native app usage.

## Contributing

🚀 Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request.

## Support

📧 For any issues or questions, please reach out to our support team via email: support@example.com

## License

📄 This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

🙏 Special thanks to the open-source community and contributors who make projects like this possible.
