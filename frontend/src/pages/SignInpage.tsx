import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
	Card,
	CardAction,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function SignInPage() {
	const navigate = useNavigate();
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setLoading(true);
		setError("");

		try {
			const res = await fetch("http://localhost:8000/signin", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ username, password }),
			});

			if (!res.ok) {
				const errorData = await res.json();
				throw new Error(errorData.detail || "Login failed");
			}

			const data = await res.json();
			localStorage.setItem("token", data.access_token);

			// ✅ redirect to main page
			navigate("/main");
		} catch (err: any) {
			setError(err.message || "An error occurred");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="flex min-h-screen flex-col items-center justify-center bg-background px-4">
			<h1 className="mb-6 text-3xl font-semibold tracking-tight text-center">
				Read2Speech — Sign In
			</h1>

			<Card className="w-full max-w-sm">
				<CardHeader>
					<CardTitle>Login to your account</CardTitle>
					<CardDescription>Enter your username and password</CardDescription>
					<CardAction>
						<Button variant="link" onClick={() => navigate("/signup")}>
							Sign Up
						</Button>
					</CardAction>
				</CardHeader>

				<CardContent>
					<form onSubmit={handleSubmit}>
						<div className="flex flex-col gap-6">
							<div className="grid gap-2">
								<Label htmlFor="username">Username</Label>
								<Input
									id="username"
									type="text"
									placeholder="your_username"
									required
									value={username}
									onChange={(e) => setUsername(e.target.value)}
								/>
							</div>

							<div className="grid gap-2">
								<Label htmlFor="password">Password</Label>
								<Input
									id="password"
									type="password"
									required
									value={password}
									onChange={(e) => setPassword(e.target.value)}
								/>
							</div>

							{error && (
								<div className="text-sm text-red-500 text-center">{error}</div>
							)}
						</div>
					</form>
				</CardContent>

				<CardFooter className="flex-col gap-2">
					<Button
						type="submit"
						className="w-full"
						onClick={handleSubmit}
						disabled={loading}
					>
						{loading ? "Logging in..." : "Login"}
					</Button>
				</CardFooter>
			</Card>
		</div>
	);
}
