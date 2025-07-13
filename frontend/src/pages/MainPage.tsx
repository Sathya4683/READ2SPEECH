import { useEffect, useState } from "react";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface FinishedItem {
	website: string;
	download_link: string;
}

function getUsernameFromJWT(): string | null {
	const token = localStorage.getItem("token");
	if (!token) return null;

	try {
		const payload = JSON.parse(atob(token.split(".")[1]));
		return payload.user || null;
	} catch (e) {
		return null;
	}
}

export default function MainPage() {
	const username = getUsernameFromJWT();
	const [link, setLink] = useState("");
	const [sendMails, setSendMails] = useState(false);
	const [webpages, setWebpages] = useState<string[]>([]);
	const [finished, setFinished] = useState<FinishedItem[]>([]);

	// Fetch user data on mount
	useEffect(() => {
		if (!username) return;

		fetch(`http://localhost:8000/userdetails/${username}`)
			.then((res) => res.json())
			.then((data) => {
				setWebpages(data.webpages || []);
				setFinished(data.finished || []);
				setSendMails(data.send_mail || false);
			})
			.catch(console.error);
	}, [username]);

	// Handle link submit
	const handleSend = async () => {
		if (!link.trim()) return;
		await fetch("http://localhost:8000/add", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username, link }),
		});
		setLink("");
	};

	// Handle mail toggle save
	const handleSaveMailPref = async () => {
		await fetch("http://localhost:8000/set-email-preference", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username, send_mails: sendMails }),
		});
	};

	return (
		<div className="p-6 space-y-10">
			<h1 className="text-3xl font-semibold tracking-tight text-center">
				Welcome, {username}
			</h1>

			{/* Link submission */}
			<div className="flex items-center gap-4 max-w-xl mx-auto">
				<Input
					type="text"
					placeholder="Enter website link"
					value={link}
					onChange={(e) => setLink(e.target.value)}
				/>
				<Button onClick={handleSend}>Send</Button>
			</div>

			{/* Mail preference toggle */}
			<div className="flex items-center justify-center gap-4">
				<div className="flex items-center space-x-2">
					<Switch
						id="send-mails"
						checked={sendMails}
						onCheckedChange={setSendMails}
					/>
					<Label htmlFor="send-mails">Send email when done</Label>
				</div>
				<Button onClick={handleSaveMailPref}>Save</Button>
			</div>

			{/* Finished audio files scroll area */}
			<div className="max-w-3xl mx-auto">
				<h2 className="text-xl font-medium mb-2">Your Audio Files</h2>
				<ScrollArea className="h-64 w-full rounded-md border">
					<div className="p-4">
						{finished.map((item) => (
							<div key={item.website}>
								<div className="flex items-center justify-between">
									<div className="text-sm font-medium">{item.website}</div>
									<a
										href={item.download_link}
										download
										target="_blank"
										rel="noopener noreferrer"
									>
										<Button size="sm">Download</Button>
									</a>
								</div>
								<Separator className="my-2" />
							</div>
						))}
						{finished.length === 0 && (
							<div className="text-muted-foreground text-sm text-center">
								No audio files yet.
							</div>
						)}
					</div>
				</ScrollArea>
			</div>

			{/* Submitted links scroll area */}
			<div className="max-w-3xl mx-auto">
				<h2 className="text-xl font-medium mb-2">Submitted Links</h2>
				<ScrollArea className="h-48 w-full rounded-md border">
					<div className="p-4">
						{webpages.map((url, idx) => (
							<div key={idx}>
								<div className="text-sm">{url}</div>
								<Separator className="my-2" />
							</div>
						))}
						{webpages.length === 0 && (
							<div className="text-muted-foreground text-sm text-center">
								No links submitted yet.
							</div>
						)}
					</div>
				</ScrollArea>
			</div>
		</div>
	);
}
