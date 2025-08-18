import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import axios from "axios";
import {
  PlusCircle,
  Edit,
  Trash2,
  Info,
  ArrowLeft,
  Loader,
  Ticket,
} from "lucide-react";
import "./App.css";

// Import components
import SplashScreen from "./components/SplashScreen";
import Auth from "./components/Auth";
import OnboardingFlow from "./components/OnboardingFlow";
import Dashboard from "./components/Dashboard";
import Profile from "./components/Profile";
import ChatInterface from "./components/ChatInterface";
import VideoLessons from "./components/VideoLessons";
import ConsciousnessTimeline from "./components/ConsciousnessTimeline";

// customer support system imports
import SupportTicketForm from "./components/customer_support_system/SupportTicket";
import CustomerList from "./components/customer_support_system/CustomerList";
import InteractionList from "./components/customer_support_system/InteractionList";
import SupportTicketList from "./components/customer_support_system/SupportTicketList";

// Define API base URL
import { Loader } from "lucide-react";
import CustomerForm from "./components/customer_support_system/Customer";
import InteractionForm from "./components/customer_support_system/InteractionForm";
import LoadingSpinner from "./components/customer_support_system/Utility";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth Context
const AuthContext = React.createContext();

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showSplash, setShowSplash] = useState(true);

  // Customer support system state
  const [customers, setCustomers] = useState([]);
  const [interactions, setInteractions] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [currentView, setCurrentView] = useState("customers"); // "customers", "interactions", "tickets"
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [message, setMessage] = useState("");

  // Function to show message box
  const showMessageBox = (message, type, onConfirm = null) => {
    setMessage({ message, type, onConfirm });
  };

  // Function to close message box
  const closeMessageBox = (confirmed = false) => {
    if (message && message.onConfirm) {
      message.onConfirm(confirmed);
    }
    setMessage(null);
  };

  // Function to fetch customers
  const fetchCustomers = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/customers`);
      setCustomers(response.data);
    } catch (error) {
      console.error("Error fetching customers:", error);
      showMessageBox("Error fetching customers. Please try again.", "error");
    } finally {
      setLoading(false);
    }
  };

  // Function to fetch interactions for a customer
  const fetchInteractions = async (customerId) => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${API}/interactions/?customer_id=${customerId}`
      );
      setInteractions(response.data);
    } catch (error) {
      console.error("Error fetching interactions:", error);
      showMessageBox("Error fetching interactions. Please try again.", "error");
    } finally {
      setLoading(false);
    }
  };

  // New function to fetch support tickets

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/tickets/`);
      setTickets(response.data);
    } catch (error) {
      console.error("Error fetching support tickets:", error);
      showMessageBox(
        "Error fetching support tickets. Please try again.",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchCustomers();
    fetchTickets(); // Fetch tickets on initial load
  }, []);

  // Customer Handlers
  const handleAddCustomer = async (customerData) => {
    setLoading(true);
    try {
      await axios.post(`${API}/customers/`, customerData);
      showMessageBox("success", "Customer added successfully");
      setCurrentView("customers");
      fetchCustomers();
    } catch (error) {
      console.error("Error adding customer:", error);
      showMessageBox(
        `Error adding customer: ${error.response?.data?.detail || error.message}`,
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateCustomer = async (customerData) => {
    setLoading(true);
    try {
      await axios.put(`${API}/customers/${customerData.id}/`, customerData);
      showMessageBox("success", "Customer updated successfully");
      setCurrentView("customers");
      fetchCustomers(); // refresh customer list
    } catch (error) {
      console.error("Error updating customer:", error);
      showMessageBox(
        `Error updating customer: ${error.response?.data?.detail || error.message}`,
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteCustomer = async (customerId) => {
    showMessageBox(
      "confirm",
      "Are you sure you want to delete this customer?",
      async (confirmed) => {
        if (confirmed) {
          setLoading(true);
          try {
            await axios.delete(`${API}/customers/${customerId}/`);
            showMessageBox("success", "Customer deleted successfully");
            fetchCustomers(); // refresh customer list
          } catch (error) {
            console.error("Error deleting customer:", error);
            showMessageBox(
              `Error deleting customer: ${error.response?.data?.detail || error.message}`,
              "error"
            );
          } finally {
            setLoading(false);
          }
        }
      }
    );
  };

  const handleViewInteractions = (customer) => {
    setSelectedCustomer(customer);
    setCurrentView("interactions");
    fetchInteractions(customer.id);
  };

  // Interaction Handlers

  const handleAddInteraction = async (interactionData) => {
    setLoading(true);
    try {
      await axios.post(`${API}/interactions/`, interactionData);
      showMessageBox("success", "Interaction added successfully");
      fetchInteractions(selectedCustomer.id); // refresh interactions for current customer
    } catch (error) {
      console.error("Error adding interaction:", error);
      showMessageBox(
        `Error adding interaction: ${error.response?.data?.detail || error.message}`,
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  // Support Ticket Handlers
  const handleCreateTicket = async (ticketData) => {
    setLoading(true);
    try {
      await axios.post(`${API}/tickets/`, ticketData);
      showMessageBox("success", "Support ticket created successfully");
      fetchTickets(); // refresh ticket list
      setCurrentView("tickets");
    } catch (error) {
      console.error("Error creating support ticket:", error);
      showMessageBox(
        `Error creating support ticket: ${error.response?.data?.detail || error.message}`,
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTicket = async (ticketData) => {
    setLoading(true);
    try {
      await axios.put(`${API}/tickets/${ticketData.id}/`, ticketData);
      showMessageBox("success", "Support ticket updated successfully");
      fetchTickets(); // refresh ticket list
      setCurrentView("tickets");
    } catch (error) {
      console.error("Error updating support ticket:", error);
      showMessageBox(
        `Error updating support ticket: ${error.response?.data?.detail || error.message}`,
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTicket = async (ticketId) => {
    setLoading(true);
    try {
      await axios.delete(`${API}/tickets/${ticketId}/`);
      showMessageBox("success", "Support ticket deleted successfully");
      fetchTickets(); // refresh ticket list
    } catch (error) {
      console.error("Error deleting support ticket:", error);
      showMessageBox(
        `Error deleting support ticket: ${error.response?.data?.detail || error.message}`,
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  // Render Logic based on current view

  const renderCurrentView = () => {
    switch (currentView) {
      case "customers":
        return (
          <>
            <div className="flex justify-between items-center mb-4">
              <button
                onClick={() => setCurrentView("addCustomer")}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <PlusCircle className="w-5 h-5 mr-2" />
                Add Customer
              </button>
            </div>
            <CustomerList
              customers={customers}
              onEditCustomer={handleUpdateCustomer}
              onDeleteCustomer={handleDeleteCustomer}
              onViewInteractions={handleViewInteractions}
            />
          </>
        );
      case "addCustomer":
        return (
          <CustomerForm
            onSubmit={handleAddCustomer}
            onCancel={() => setCurrentView("customers")}
          />
        );
      case "editCustomer":
        return (
          <CustomerForm
            customer={selectedCustomer}
            onSubmit={handleUpdateCustomer}
            onCancel={() => setCurrentView("customers")}
          />
        );
      case "viewInteractions":
        return (
          <InteractionList
            customerName={selectedCustomer?.name}
            interactions={interactions}
            onBackToCustomers={() => {
              setCurrentView("customers");
              setSelectedCustomer(null);
              setInteractions([]);
            }}
          />
        );
      case "addInteraction":
        return (
          <InteractionForm
            customerId={selectedCustomer?.id}
            onSave={handleAddInteraction}
            onCancel={() => setCurrentView("viewInteractions")}
          />
        );
      case "tickets":
        return (
          <SupportTicketList
            tickets={tickets}
            customers={customers}
            onAddTicket={() => setCurrentView("addTicket")}
            onEditTicket={(ticket) => {
              setSelectedTicket(ticket);
              setCurrentView("editTicket");
            }}
            onDeleteTicket={handleDeleteTicket}
            showMessageBox={showMessageBox} // pass Message box function
          />
        );

      case "addTicket":
        return (
          <SupportTicketForm
            customers={customers}
            onSave={handleCreateTicket}
            onCancel={() => setCurrentView("tickets")}
          />
        );
      case "editTicket":
        return (
          <SupportTicketForm
            ticket={selectedTicket}
            customers={customers}
            onSave={handleUpdateTicket}
            onCancel={() => setCurrentView("tickets")}
          />
        );
      default:
        return null;
    }
  };

  useEffect(() => {
    checkAuthStatus();

    // Show splash screen for 3 seconds
    const splashTimer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => clearTimeout(splashTimer);
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const response = await axios.get(`${API}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem("token");
      }
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, {
        email,
        password,
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      // Get user info
      const userResponse = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      setUser(userResponse.data);
      return true;
    } catch (error) {
      console.error("Login error:", error);
      return false;
    }
  };

  const register = async (email, password, fullName) => {
    try {
      const response = await axios.post(`${API}/auth/register`, {
        email,
        password,
        full_name: fullName,
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      // Get user info
      const userResponse = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      setUser(userResponse.data);
      return true;
    } catch (error) {
      console.error("Registration error:", error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white"></div>
      </div>
    );
  }

  if (showSplash) {
    return <SplashScreen onComplete={() => setShowSplash(false)} />;
  }

  return (
    <>
      <AuthContext.Provider value={{ user, login, register, logout, API }}>
        <div className="App">
          <BrowserRouter>
            <Routes>
              {!user ? (
                <>
                  <Route path="/auth" element={<Auth />} />
                  <Route path="*" element={<Navigate to="/auth" replace />} />
                </>
              ) : !user.personality_test_completed ? (
                <>
                  <Route path="/onboarding" element={<OnboardingFlow />} />
                  <Route
                    path="*"
                    element={<Navigate to="/onboarding" replace />}
                  />
                </>
              ) : (
                <>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/chat" element={<ChatInterface />} />
                  <Route path="/videos" element={<VideoLessons />} />
                  <Route
                    path="/consciousness"
                    element={<ConsciousnessTimeline />}
                  />
                  <Route
                    path="*"
                    element={<Navigate to="/dashboard" replace />}
                  />
                </>
              )}
            </Routes>
          </BrowserRouter>
        </div>
      </AuthContext.Provider>

      {/* Customer Support */}
      <div className="min-h-screen bg-gray-100 font-sans antialiased text-gray-900 p-4 sm:p-6 lg:p-8">
        <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-6 rounded-lg shadow-md mb-8">
          <h1 className="text-4xl font-extrabold text-center tracking-tight">
            Customer Support
          </h1>
          <p className="text-center text-blue-100 mt-2 text-lg">
            Manage customers, interactions, and support tickets
          </p>
          <nav className="mt-6 flex justify-center space-x-6">
            <button
              onClick={() => setCurrentView("customers")}
              className={`flex items-center px-4 py-2 rounded-md transition duration-150 ease-in-out ${
                currentView.startsWith("customer") ||
                currentView.startsWith("interaction")
                  ? "bg-blue-800 text-white shadow-lg"
                  : "text-blue-200 hover:bg-blue-700 hover:text-white"
              }`}
            >
              <Info className="h-5 w-5 mr-2" />
              Customers
            </button>
            <button
              onClick={() => setCurrentView("tickets")}
              className={`px-4 py-2 rounded-md ${
                currentView === "tickets"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-800 hover:bg-gray-300"
              }`}
            >
              Support Tickets
            </button>
          </nav>
        </header>

        <main className="container mx-auto">
          {loading && <LoadingSpinner />}
          {message && (
            <showMessageBox
              type={message.type}
              message={message.message}
              onClose={closeMessageBox}
              onConfirm={message.onConfirm}
            />
          )}
          {!loading && renderContent()}
        </main>
        <footer className="mt-8 text-center text-gray-600">
          <p>
            {new Date().getFullYear()} © 2025 Evolance. All rights reserved.
          </p>
        </footer>
      </div>
    </>
  );
}

export default App;
export { AuthContext };
