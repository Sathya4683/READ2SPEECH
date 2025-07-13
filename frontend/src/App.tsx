import {
	BrowserRouter as Router,
	Routes,
	Route,
	Navigate,
} from "react-router-dom";
import SignInPage from "./pages/SignInpage";
import SignUpPage from "./pages/SignUpPage";
import MainPage from "./pages/MainPage";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Navigate to="/signin" replace />} />
				<Route path="/signin" element={<SignInPage />} />
				<Route path="/signup" element={<SignUpPage />} />
				<Route path="/main" element={<MainPage />} />
			</Routes>
		</Router>
	);
}

export default App;
