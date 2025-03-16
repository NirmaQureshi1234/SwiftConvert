import streamlit as st
import requests

st.set_page_config(page_title="Multi-Unit Converter", page_icon="")

st.markdown(
    """
    <style>
        /* General body text color */
        body { background-color: #0e0e0e; color: white; font-family: 'Poppins', sans-serif; }
        
        /* Streamlit app background */
        .stApp { background-color: #0e0e0e; }
        
        /* Sidebar background and text color */
        .stSidebar { 
            background-color: #141414; 
            color: white !important; 
        }
        
        /* Sidebar text color */
        .stSidebar .stRadio label, 
        .stSidebar .stMarkdown, 
        .stSidebar .stText, 
        .stSidebar .stNumberInput label, 
        .stSidebar .stSelectbox label, 
        .stSidebar .stTextInput label, 
        .stSidebar .stSlider label {
            color: white !important;
        }
        
        /* Button styling */
        .stButton > button { background-color: #ff4757; color: white; border-radius: 10px; font-size: 18px; }
        
        /* Input fields (selectbox, text input, number input) */
        .stSelectbox, .stTextInput, .stNumberInput { background-color: #222; color: white; border-radius: 8px; }
        
        /* Title styling */
        .title { color: #f1c40f; text-align: center; font-size: 40px; font-weight: bold; text-shadow: 2px 2px #ff4757; }
        
        /* Conversion box styling */
        .convert-box { background-color: #222; padding: 20px; border-radius: 12px; box-shadow: 0px 0px 15px #ff4757; }
        
        /* Streamlit default text color (gray) changed to white */
        .stMarkdown, .stText, .stNumberInput label, .stSelectbox label, .stTextInput label, .stSlider label {
            color: white !important;
        }
        
        /* Footer text color */
        footer { color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="title">⚡ Multi-Unit Converter</p>', unsafe_allow_html=True)
st.write("Convert Length, Weight, Temperature & Currency in Real-Time!")

option = st.sidebar.radio("Select a Conversion Type", ("📏 Length", "⚖️ Weight", "🌡 Temperature", "💰 Currency"))

st.markdown('<div class="convert-box">', unsafe_allow_html=True)

# Length Converter
if option == "📏 Length":
    st.subheader("📏 Length Converter")
    length_units = {"Meters": 1, "Kilometers": 1000, "Centimeters": 0.01, "Feet": 0.3048, "Inches": 0.0254, "Miles": 1609.34}
    from_unit = st.selectbox("From:", list(length_units.keys()))
    to_unit = st.selectbox("To:", list(length_units.keys()))
    value = st.number_input("Enter Value:", min_value=0.0, step=0.1)
    
    if st.button("Convert 🔄"):
        result = (value * length_units[from_unit]) / length_units[to_unit]
        st.success(f"{value} {from_unit} = {round(result, 4)} {to_unit}")

# Weight Converter
elif option == "⚖️ Weight":
    st.subheader("⚖️ Weight Converter")
    weight_units = {"Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495}
    from_unit = st.selectbox("From:", list(weight_units.keys()))
    to_unit = st.selectbox("To:", list(weight_units.keys()))
    value = st.number_input("Enter Value:", min_value=0.0, step=0.1)
    
    if st.button("Convert 🔄"):
        result = (value * weight_units[from_unit]) / weight_units[to_unit]
        st.success(f"{value} {from_unit} = {round(result, 4)} {to_unit}")

# Temperature Converter
elif option == "🌡 Temperature":
    st.subheader("🌡 Temperature Converter")
    temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
    from_unit = st.selectbox("From:", temp_units)
    to_unit = st.selectbox("To:", temp_units)
    value = st.number_input("Enter Value:", step=0.1)

    def convert_temperature(value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
        elif from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32

    if st.button("Convert 🔄"):
        result = convert_temperature(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {round(result, 2)} {to_unit}")

# Currency Converter
elif option == "💰 Currency":
    st.subheader("💰 Currency Converter")
    try:
        # Fetch currency rates from exchangerate-api.com
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        
        if data["result"] == "success":
            currencies = list(data["rates"].keys())
            from_currency = st.selectbox("From Currency:", currencies)
            to_currency = st.selectbox("To Currency:", currencies)
            amount = st.number_input("Enter Amount:", min_value=0.0, step=1.0)

            if st.button("Convert 🔄"):
                if from_currency == to_currency:
                    result = amount
                else:
                    rate = data["rates"][to_currency] / data["rates"][from_currency]
                    result = amount * rate
                st.success(f"{amount} {from_currency} = {round(result, 2)} {to_currency}")
        else:
            st.error("Failed to fetch currency rates. Please try again later.")
    except Exception as e:
        st.error(f"Error fetching currency rates: {e}. Please check your internet connection or try again later.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("Made by NIRMA QURESHI 🖤")
