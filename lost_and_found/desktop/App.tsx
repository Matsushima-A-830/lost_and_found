import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginWindow from "./pages/LoginWindow";
import MainDashboard from "./pages/MainDashboard";
import ItemRegistrationForm from "./pages/ItemRegistrationForm";
import ItemSearchPage from "./pages/ItemSearchPage";
import ItemDetailDrawer from "./pages/ItemDetailDrawer";
import PoliceReportWizard from "./pages/PoliceReportWizard";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginWindow />} />
        <Route path="/dashboard" element={<MainDashboard />} />
        <Route path="/register" element={<ItemRegistrationForm />} />
        <Route path="/search" element={<ItemSearchPage />} />
        <Route path="/item/:id" element={<ItemDetailDrawer />} />
        <Route path="/police-report" element={<PoliceReportWizard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
