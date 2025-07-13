import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
	Card,
	CardHeader,
	CardTitle,
	CardDescription,
	CardContent,
	CardFooter,
	CardAction,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function SignUpPage() {
	const navigate = useNavigate();

	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError("");

		if (password !== confirmPassword) {
			setError("Passwords do not match");
			return;
		}

		setLoading(true);
		try {
			const res = await fetch("http://localhost:8000/signup", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ username, password }),
			});

			if (!res.ok) {
				const errorData = await res.json();
				throw new Error(errorData.detail || "Signup failed");
			}

			// Success: redirect to login
			navigate("/signin");
		} catch (err: any) {
			setError(err.message || "An error occurred");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="flex min-h-screen flex-col items-center justify-center bg-background px-4">
			<h1 className="mb-6 text-3xl font-semibold tracking-tight text-center">
				Read2Speech — Sign Up
			</h1>

			<Card className="w-full max-w-sm">
				<CardHeader>
					<CardTitle>Create a new account</CardTitle>
					<CardDescription>Enter your details to get started</CardDescription>
					<CardAction>
						<Button variant="link" onClick={() => navigate("/signin")}>
							Already have an account?
						</Button>
					</CardAction>
				</CardHeader>

				<CardContent>
					<form onSubmit={handleSubmit}>
						<div className="flex flex-col gap-6">
							<div className="grid gap-2">
								<Label htmlFor="username">Email Address</Label>
								<Input
									id="username"
									type="email"
									placeholder="you@example.com"
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

							<div className="grid gap-2">
								<Label htmlFor="confirm-password">Confirm Password</Label>
								<Input
									id="confirm-password"
									type="password"
									required
									value={confirmPassword}
									onChange={(e) => setConfirmPassword(e.target.value)}
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
						{loading ? "Creating account..." : "Sign Up"}
					</Button>
				</CardFooter>
			</Card>
		</div>
	);
}
